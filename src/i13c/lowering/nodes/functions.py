from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Tuple, Type

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.callsites import lower_callsite
from i13c.lowering.nodes.registers import caller_saved
from i13c.lowering.typing.blocks import Block, BlockInstruction, Registers
from i13c.lowering.typing.flows import BlockId, EpilogueFlow, FlowId, PrologueFlow
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    JumpTerminator,
    TrapTerminator,
)
from i13c.semantic.model import SemanticGraph
from i13c.semantic.rules import SemanticRules
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.indices.controlflows import (
    FlowEntry,
    FlowExit,
    FlowGraph,
    FlowNode,
)

# the goal of this module is to convert all active functions into blocks with instructions;
# each block can have forward and backward edges and each function has its entries and exits;
# additionally exactly one entrypoint must be found;


def verify(rules: SemanticRules, **kwargs: Dict[str, Any]) -> bool:
    return rules.count() == 0


def configure_functions() -> GraphNode:
    return GraphNode(
        builder=lower_active_functions,
        constraint=verify,
        produces=(
            "llvm/entrypoint",
            "llvm/blocks",
            "llvm/blocks/forward",
            "llvm/blocks/backward",
            "llvm/blocks/instructions",
            "llvm/registers/inputs",
            "llvm/registers/clobbers",
            "llvm/functions/entries",
            "llvm/functions/exits",
        ),
        requires=frozenset(
            {
                ("graph", "semantic/graph"),
                ("rules", "rules/semantic"),
            }
        ),
    )


@dataclass(kw_only=True)
class Context:
    graph: SemanticGraph
    generator: Generator
    entrypoint: Optional[BlockId]

    blocks: Dict[BlockId, Block]
    instructions: Dict[BlockId, List[BlockInstruction]]

    inputs: Dict[BlockId, Registers]
    clobbers: Dict[BlockId, Registers]

    forward: Dict[BlockId, List[BlockId]]
    backward: Dict[BlockId, List[BlockId]]

    entries: Dict[FunctionId, BlockId]
    exits: Dict[FunctionId, BlockId]

    @staticmethod
    def empty(graph: SemanticGraph) -> "Context":
        return Context(
            graph=graph,
            generator=graph.generator,
            entrypoint=None,
            blocks={},
            instructions={},
            inputs={},
            clobbers={},
            forward={},
            backward={},
            entries={},
            exits={},
        )


def lower_active_functions(
    graph: SemanticGraph,
    **kwargs: Dict[str, Any],
) -> Tuple[
    Optional[BlockId],
    OneToOne[BlockId, Block],
    OneToMany[BlockId, BlockId],
    OneToMany[BlockId, BlockId],
    OneToMany[BlockId, BlockInstruction],
    OneToOne[BlockId, Registers],
    OneToOne[BlockId, Registers],
    OneToOne[FunctionId, BlockId],
    OneToOne[FunctionId, BlockId],
]:
    ctx = Context.empty(graph)

    # lower all live callables
    for fid in graph.callable_live:
        if isinstance(fid, FunctionId):
            # find flowgraph and generate blocks
            flowgraph = graph.live.flowgraph_by_function.get(fid)
            block = lower_function_flow(ctx, fid, flowgraph)

            # returned block may be an entrypoint
            if graph.live.entrypoints.contains(fid):
                ctx.entrypoint = block

    # entry has to be found
    assert ctx.entrypoint is not None

    # success
    return (
        ctx.entrypoint,
        OneToOne[BlockId, Block].instance(ctx.blocks),
        OneToMany[BlockId, BlockId].instance(ctx.forward),
        OneToMany[BlockId, BlockId].instance(ctx.backward),
        OneToMany[BlockId, BlockInstruction].instance(ctx.instructions),
        OneToOne[BlockId, Registers].instance(ctx.inputs),
        OneToOne[BlockId, Registers].instance(ctx.clobbers),
        OneToOne[FunctionId, BlockId].instance(ctx.entries),
        OneToOne[FunctionId, BlockId].instance(ctx.exits),
    )


def lower_flow_entry(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: FlowEntry,
) -> FlowNodeContext:
    # obtain successors
    successors = flow.forward.get(node, [])
    assert len(successors) == 1

    # create jump terminator to successor
    terminator = JumpTerminator(target=mapping[successors[0]])

    # prepare entry instructions
    iid = FlowId(value=ctx.generator.next())
    instructions: List[BlockInstruction] = [(iid, PrologueFlow(target=fid))]

    # register entry block
    ctx.entries[fid] = mapping[node]

    # create empty block with jump
    return FlowNodeContext(
        block=Block(origin=fid, terminator=terminator),
        instructions=instructions,
        inputs=Registers.instance(caller_saved()),
        clobbers=Registers.empty(),
    )


def lower_flow_exit(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: FlowExit,
) -> FlowNodeContext:
    # register exit block
    ctx.exits[fid] = mapping[node]

    # prepare exit instructions
    iid = FlowId(value=ctx.generator.next())
    instructions: List[BlockInstruction] = [(iid, EpilogueFlow(target=fid))]

    # create empty block with exit
    return FlowNodeContext(
        block=Block(origin=fid, terminator=ExitTerminator()),
        instructions=instructions,
        inputs=Registers.empty(),
        clobbers=Registers.empty(),
    )


def lower_flow_callsite(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: CallSiteId,
) -> FlowNodeContext:
    # obtain successors
    successors = flow.forward.get(node, [])
    assert len(successors) in (0, 1)

    # create jump or trap
    terminator = (
        JumpTerminator(target=mapping[successors[0]])
        if len(successors) == 1
        else TrapTerminator()
    )

    # lower callsite instructions and clobbers
    instructions, clobbers = lower_callsite(ctx.graph, node)

    # lower callsite block
    return FlowNodeContext(
        block=Block(origin=node, terminator=terminator),
        instructions=instructions,
        inputs=Registers.empty(),
        clobbers=Registers.instance(clobbers),
    )


@dataclass
class FlowNodeContext:
    block: Block
    instructions: List[BlockInstruction]
    inputs: Registers
    clobbers: Registers


class FlowNodeLowerer(Protocol):
    def __call__(
        self,
        ctx: Context,
        fid: FunctionId,
        flow: FlowGraph,
        mapping: Dict[FlowNode, BlockId],
        node: FlowNode,
    ) -> FlowNodeContext: ...


DISPATCH_TABLE: Dict[Type[FlowNode], FlowNodeLowerer] = {
    FlowEntry: lower_flow_entry,
    FlowExit: lower_flow_exit,
    CallSiteId: lower_flow_callsite,
}  # pyright: ignore[reportAssignmentType]


def lower_function_flow(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
) -> BlockId:
    mapping: Dict[FlowNode, BlockId] = {}

    # assign ID to each FlowNode
    for node in flow.nodes():
        mapping[node] = BlockId(value=ctx.generator.next())
        ctx.forward[mapping[node]] = []
        ctx.backward[mapping[node]] = []

    # lower each FlowNode
    for node in flow.nodes():
        output = DISPATCH_TABLE[type(node)](ctx, fid, flow, mapping, node)

        # register block, instructions and registers
        ctx.blocks[mapping[node]] = output.block
        ctx.instructions[mapping[node]] = output.instructions
        ctx.inputs[mapping[node]] = output.inputs
        ctx.clobbers[mapping[node]] = output.clobbers

    # wire forward edges
    for node, successors in flow.forward.items():
        ctx.forward[mapping[node]].extend([mapping[next] for next in successors])

    # wire backward edges
    for node, predecessors in flow.backward.items():
        ctx.backward[mapping[node]].extend([mapping[prev] for prev in predecessors])

    return mapping[flow.entry]
