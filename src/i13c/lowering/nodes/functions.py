from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Tuple, Type

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.callsites import lower_callsite
from i13c.lowering.nodes.registers import caller_saved
from i13c.lowering.typing.blocks import Block, BlockInstruction, Registers
from i13c.lowering.typing.flows import BlockId, EpilogueFlow, PrologueFlow
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


def configure_functions() -> GraphNode:
    return GraphNode(
        builder=lower_active_functions,
        produces=(
            "llvm/entrypoint",
            "llvm/blocks",
            "llvm/forward",
            "llvm/backward",
            "llvm/entries",
            "llvm/exits",
        ),
        requires=frozenset({("graph", "semantic/graph"), ("rules", "rules/semantic")}),
    )


@dataclass(kw_only=True)
class Context:
    graph: SemanticGraph
    generator: Generator
    entrypoint: Optional[BlockId]

    nodes: Dict[BlockId, Block]
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
            nodes={},
            forward={},
            backward={},
            entries={},
            exits={},
        )


def lower_active_functions(
    graph: SemanticGraph,
    rules: SemanticRules,
) -> Tuple[
    Optional[BlockId],
    OneToOne[BlockId, Block],
    OneToMany[BlockId, BlockId],
    OneToMany[BlockId, BlockId],
    OneToOne[FunctionId, BlockId],
    OneToOne[FunctionId, BlockId],
]:
    ctx = Context.empty(graph)

    # lower all live callables
    if rules.count() == 0:
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
        OneToOne[BlockId, Block].instance(ctx.nodes),
        OneToMany[BlockId, BlockId].instance(ctx.forward),
        OneToMany[BlockId, BlockId].instance(ctx.backward),
        OneToOne[FunctionId, BlockId].instance(ctx.entries),
        OneToOne[FunctionId, BlockId].instance(ctx.exits),
    )


def lower_flow_entry(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: FlowEntry,
) -> Block:
    # obtain successors
    successors = flow.forward.get(node, [])
    assert len(successors) == 1

    # create jump terminator to successor
    terminator = JumpTerminator(target=mapping[successors[0]])

    # prepare entry instructions
    instructions: List[BlockInstruction] = [PrologueFlow(target=fid)]

    # register entry block
    ctx.entries[fid] = mapping[node]

    # create empty block with jump
    return Block(
        origin=fid,
        instructions=instructions,
        registers=Registers.provides(caller_saved()),
        terminator=terminator,
    )


def lower_flow_exit(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: FlowExit,
) -> Block:
    # register exit block
    ctx.exits[fid] = mapping[node]

    # prepare exit instructions
    instructions: List[BlockInstruction] = [EpilogueFlow(target=fid)]

    # create empty block with exit
    return Block(
        origin=fid,
        instructions=instructions,
        registers=Registers.empty(),
        terminator=ExitTerminator(),
    )


def lower_flow_callsite(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: CallSiteId,
) -> Block:
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
    return Block(
        origin=node,
        terminator=terminator,
        instructions=instructions,
        registers=Registers.clobbers(clobbers),
    )


class FlowNodeLowerer(Protocol):
    def __call__(
        self,
        ctx: Context,
        fid: FunctionId,
        flow: FlowGraph,
        mapping: Dict[FlowNode, BlockId],
        node: FlowNode,
    ) -> Block: ...


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
        ctx.nodes[mapping[node]] = DISPATCH_TABLE[type(node)](
            ctx, fid, flow, mapping, node
        )

    # wire forward edges
    for node, successors in flow.forward.items():
        ctx.forward[mapping[node]].extend([mapping[next] for next in successors])

    # wire backward edges
    for node, predecessors in flow.backward.items():
        ctx.backward[mapping[node]].extend([mapping[prev] for prev in predecessors])

    return mapping[flow.entry]
