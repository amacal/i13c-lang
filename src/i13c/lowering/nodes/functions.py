from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Tuple, Type

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.callsites import lower_callsite
from i13c.lowering.typing.blocks import Block, BlockInstruction
from i13c.lowering.typing.flows import (
    BlockId,
    EpilogueFlow,
    FlowId,
    ImmediateFlow,
    PrologueFlow,
    SnapshotFlow,
)
from i13c.lowering.typing.instructions import (
    InstructionEntry,
    InstructionId,
    MovOffImm,
    MovOffReg,
    Nop,
)
from i13c.lowering.typing.registers import VirtualRegister, name_to_reg
from i13c.lowering.typing.stacks import StackFrame
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    JumpTerminator,
    TrapTerminator,
)
from i13c.semantic.model import SemanticGraph
from i13c.semantic.rules import SemanticRules
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.literals import Hex, LiteralId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.indices.controlflows import (
    FlowEntry,
    FlowExit,
    FlowGraph,
    FlowNode,
)
from i13c.semantic.typing.indices.variables import VariableId
from i13c.semantic.typing.resolutions.values import ValueResolution

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
            "llvm/instructions",
            "llvm/functions/entries",
            "llvm/functions/exits",
        ),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("graph", "semantic/graph"),
                ("values", "resolutions/values"),
                ("rules", "rules/semantic"),
                ("registers", "llvm/registers"),
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

    registers: OneToOne[VariableId, VirtualRegister]
    values: OneToOne[ValueId, ValueResolution]

    forward: Dict[BlockId, List[BlockId]]
    backward: Dict[BlockId, List[BlockId]]

    entries: Dict[FunctionId, BlockId]
    exits: Dict[FunctionId, BlockId]

    @staticmethod
    def empty(
        graph: SemanticGraph,
        generator: Generator,
        values: OneToOne[ValueId, ValueResolution],
        registers: OneToOne[VariableId, VirtualRegister],
    ) -> Context:
        return Context(
            graph=graph,
            generator=generator,
            entrypoint=None,
            blocks={},
            instructions={},
            values=values,
            registers=registers,
            forward={},
            backward={},
            entries={},
            exits={},
        )


def lower_active_functions(
    generator: Generator,
    graph: SemanticGraph,
    registers: OneToOne[VariableId, VirtualRegister],
    values: OneToOne[ValueId, ValueResolution],
    **kwargs: Dict[str, Any],
) -> Tuple[
    Optional[BlockId],
    OneToOne[BlockId, Block],
    OneToMany[BlockId, BlockId],
    OneToMany[BlockId, BlockId],
    OneToMany[BlockId, BlockInstruction],
    OneToOne[FunctionId, BlockId],
    OneToOne[FunctionId, BlockId],
]:
    ctx = Context.empty(graph, generator, values, registers)

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

    # generate virtual registers for parameters
    for idx, pid in enumerate(ctx.graph.basic.functions.get(fid).parameters):

        # get a variable behind the fucntion parameter
        variable = ctx.graph.indices.variables_by_parameter.get(pid)

        # generate virtual move flow between physical and virtual register
        iid = FlowId(value=ctx.generator.next())
        instr = SnapshotFlow(dst=ctx.registers.get(variable).ref(), src=idx)

        # append it
        instructions.append((iid, instr))

    # register entry block
    ctx.entries[fid] = mapping[node]

    # create empty block with jump
    return FlowNodeContext(
        block=Block(origin=fid, terminator=terminator),
        instructions=instructions,
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

    # lower callsite block
    return FlowNodeContext(
        block=Block(origin=node, terminator=terminator),
        instructions=lower_callsite(ctx.generator, ctx.graph, node, ctx.registers),
    )


def lower_flow_value(
    ctx: Context,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: ValueId,
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

    # prepare instructions
    instructions: List[BlockInstruction] = []

    resolution = ctx.values.get(node)
    assert resolution.accepted is not None

    if isinstance(resolution.accepted.binding, LiteralId):
        literal = ctx.graph.basic.literals.get(resolution.accepted.binding)
        assert isinstance(literal.target, Hex)

        variable = ctx.graph.indices.variables_by_parameter.get(node)
        register = ctx.registers.get(variable)

        imm = literal.target.value
        dst = register.ref()

        iid = FlowId(value=ctx.generator.next())
        instr = ImmediateFlow(imm=imm, dst=dst)

        instructions.append((iid, instr))
        # get literal

    return FlowNodeContext(
        block=Block(origin=node, terminator=terminator),
        instructions=instructions,
    )


@dataclass
class FlowNodeContext:
    block: Block
    instructions: List[BlockInstruction]


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
    ValueId: lower_flow_value,
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

    # wire forward edges
    for node, successors in flow.forward.items():
        ctx.forward[mapping[node]].extend([mapping[next] for next in successors])

    # wire backward edges
    for node, predecessors in flow.backward.items():
        ctx.backward[mapping[node]].extend([mapping[prev] for prev in predecessors])

    return mapping[flow.entry]


def configure_snapshot_patching() -> GraphNode:
    return GraphNode(
        builder=patch_snapshots,
        constraint=None,
        produces=("llvm/patches/snapshots",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("blocks", "llvm/functions/blocks"),
                ("instructions", "llvm/instructions"),
                ("stackframes", "llvm/functions/stackframes"),
            }
        ),
    )


def patch_snapshots(
    generator: Generator,
    blocks: OneToMany[FunctionId, BlockId],
    stackframes: OneToOne[FunctionId, StackFrame],
    instructions: OneToMany[BlockId, BlockInstruction],
) -> OneToOne[FlowId, InstructionEntry]:
    bindings: Dict[FlowId, InstructionEntry] = {}

    for fid, bids in blocks.items():
        for bid in bids:
            for iid, instr in instructions.get(bid):
                if not isinstance(iid, FlowId):
                    continue

                if isinstance(instr, ImmediateFlow):
                    # ImmediateFlow is referenced by FlowId
                    assert isinstance(iid, FlowId)

                    # find stackframe and get a slot entry
                    stackframe = stackframes.get(fid)
                    offset = stackframe.slot_at_register(instr.dst)

                    if offset is None:
                        bindings[iid] = (InstructionId(value=generator.next()), Nop())

                    else:
                        # append new patched binding
                        bindings[iid] = (
                            InstructionId(value=generator.next()),
                            MovOffImm(
                                dst=name_to_reg("rsp"), imm=instr.imm, off=offset * 8
                            ),
                        )

                if isinstance(instr, SnapshotFlow):
                    # SnapshotFlow is referenced by FlowId
                    assert isinstance(iid, FlowId)

                    # find stackframe and get a slot entry
                    stackframe = stackframes.get(fid)
                    offset = stackframe.slot_at_register(instr.dst)

                    if offset is None:
                        bindings[iid] = (InstructionId(value=generator.next()), Nop())

                    else:
                        # append new patched binding
                        bindings[iid] = (
                            InstructionId(value=generator.next()),
                            MovOffReg(
                                dst=name_to_reg("rsp"), src=instr.src, off=offset * 8
                            ),
                        )

    return OneToOne[FlowId, InstructionEntry].instance(bindings)
