from typing import Dict, Optional

from i13c.core.generator import Generator
from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.callsites import lower_callsite
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    FallThroughTerminator,
    TrapTerminator,
)
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.indices.flowgraphs import FlowEntry, FlowExit, FlowGraph, FlowNode


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
        ctx.edges[mapping[node]] = []

    for node in flow.nodes():
        # entry node is noop just to fall through
        if isinstance(node, FlowEntry):
            ctx.nodes[mapping[node]] = Block(
                origin=fid,
                instructions=[],
                terminator=FallThroughTerminator(),
            )

            ctx.entry[fid] = mapping[node]

        # exit node is also noop, but emits exit
        elif isinstance(node, FlowExit):
            ctx.nodes[mapping[node]] = Block(
                origin=fid,
                instructions=[],
                terminator=ExitTerminator(),
            )

            ctx.exit[fid] = mapping[node]

        # otherwise just callsite emitting either fallthrough or a trap
        else:
            has_successors = len(flow.edges.get(node) or []) > 0
            terminator = FallThroughTerminator() if has_successors else TrapTerminator()

            # lower callsite block
            ctx.nodes[mapping[node]] = lower_callsite(ctx, node, terminator)

    # wire edges
    for node, successors in flow.edges.items():
        ctx.edges[mapping[node]].extend([mapping[next] for next in successors])

    return mapping[flow.entry]
