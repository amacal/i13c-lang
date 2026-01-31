from typing import Dict, Optional, Protocol, Type

from i13c.core.generator import Generator
from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.callsites import lower_callsite
from i13c.lowering.typing.blocks import Block, Registers
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    JumpTerminator,
    TrapTerminator,
)
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.indices.controlflows import (
    FlowEntry,
    FlowExit,
    FlowGraph,
    FlowNode,
)


def lower_active_functions(ctx: LowLevelContext) -> BlockId:
    entry: Optional[BlockId] = None

    # lower all live callables
    for fid in ctx.graph.callable_live:
        if isinstance(fid, FunctionId):
            # find flowgraph and generate blocks
            flowgraph = ctx.graph.live.flowgraph_by_function.get(fid)
            block = lower_function_flow(ctx, fid, flowgraph)

            # returned block may be an entrypoint
            if ctx.graph.live.entrypoints.contains(fid):
                entry = block

    # entry has to be found
    assert entry is not None

    # success
    return entry


def lower_flow_entry(
    ctx: LowLevelContext,
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

    # register entry block
    ctx.entry[fid] = mapping[node]

    # create empty block with jump
    return Block(
        origin=fid,
        instructions=[],
        registers=Registers.empty(),
        terminator=terminator,
    )


def lower_flow_exit(
    ctx: LowLevelContext,
    fid: FunctionId,
    flow: FlowGraph,
    mapping: Dict[FlowNode, BlockId],
    node: FlowExit,
) -> Block:
    # register exit block
    ctx.exit[fid] = mapping[node]

    # create empty block with exit
    return Block(
        origin=fid,
        instructions=[],
        registers=Registers.empty(),
        terminator=ExitTerminator(),
    )


def lower_flow_callsite(
    ctx: LowLevelContext,
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
    instructions, clobbers = lower_callsite(ctx, node)

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
        ctx: LowLevelContext,
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
    ctx: LowLevelContext,
    fid: FunctionId,
    flow: FlowGraph,
) -> BlockId:
    mapping: Dict[FlowNode, BlockId] = {}
    generator: Generator = ctx.generator

    # assign ID to each FlowNode
    for node in flow.nodes():
        mapping[node] = BlockId(value=generator.next())
        ctx.forward[mapping[node]] = []
        ctx.backward[mapping[node]] = []

    # lower each FlowNode
    for node in flow.nodes():
        ctx.nodes[mapping[node]] = DISPATCH_TABLE[type(node)](
            ctx, fid, flow, mapping, node
        )

    # wire edges
    for node, successors in flow.forward.items():
        ctx.forward[mapping[node]].extend([mapping[next] for next in successors])

    return mapping[flow.entry]
