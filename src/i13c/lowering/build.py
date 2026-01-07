from typing import Dict, List, Optional, Union

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.ir import Emit, FallThrough, Instruction, Stop, Terminator
from i13c.lowering.bind import lower_callsite_bindings
from i13c.lowering.graph import LowLevelContext, LowLevelGraph
from i13c.lowering.instructions import lower_instruction
from i13c.lowering.nodes import Block, BlockId
from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.instructions import InstructionId
from i13c.sem.typing.entities.operands import Operand, OperandId
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.indices.flowgraphs import FlowEntry, FlowExit, FlowGraph, FlowNode
from i13c.sem.typing.indices.instances import Instance


def get_context(graph: SemanticGraph) -> LowLevelContext:
    return LowLevelContext(
        graph=graph,
        generator=graph.generator,
        nodes={},
        edges={},
        entry={},
        exit={},
    )


def build_low_level_graph(graph: SemanticGraph) -> LowLevelGraph:
    entry: Optional[BlockId] = None
    ctx: LowLevelContext = get_context(graph)

    # lower all callables
    for fid in graph.callable_live:
        if isinstance(fid, FunctionId):
            flowgraph = graph.live.flowgraph_by_function.get(fid)
            block = lower_function_flow(ctx, fid, flowgraph)

            if graph.live.entrypoints.contains(fid):
                entry = block

    # optionally lower snippet entrypoint
    if entry is None:
        for snid in graph.live.entrypoints.keys():
            assert isinstance(snid, SnippetId)
            entry = lower_snippet(ctx, snid)

    # entry has to be found
    assert entry is not None

    # patch CFG edges
    for bid, block in ctx.nodes.items():

        # only callsite blocks have outgoing edges
        if not isinstance(block.origin, CallSiteId):
            continue

        resolution = ctx.graph.indices.resolution_by_callsite.get(block.origin)
        acceptance = resolution.accepted[0]

        # only function callables have edges
        if not isinstance(acceptance.callable.target, FunctionId):
            continue

        # retrieve current successors
        successors = ctx.edges[bid]

        # wire callsite exit to function entry
        ctx.edges[bid] = [ctx.entry[acceptance.callable.target]]

        # only if function has an exit
        if acceptance.callable.target in ctx.exit:
            # wire function exit to current successors
            ctx.edges[ctx.exit[acceptance.callable.target]].extend(successors)

    for bid, block in ctx.nodes.items():
        if not ctx.edges[bid]:
            block.terminator = Stop()

    return LowLevelGraph(
        generator=graph.generator,
        entry=entry,
        nodes=OneToOne[BlockId, Block].instance(ctx.nodes),
        edges=OneToMany[BlockId, BlockId].instance(ctx.edges),
    )


def lower_snippet(
    ctx: LowLevelContext,
    snid: SnippetId,
) -> BlockId:

    # create instructions for snippet
    bid = BlockId(value=ctx.generator.next())
    snippet = ctx.graph.basic.snippets.get(snid)
    instrs = lower_instance_or_snippet(ctx, snippet)

    # append to graph
    ctx.edges[bid] = []
    ctx.nodes[bid] = Block(origin=snid, instructions=instrs, terminator=Stop())

    return bid


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
        # entry node is noop just transfers control
        if isinstance(node, FlowEntry):
            ctx.nodes[mapping[node]] = Block(
                origin=fid,
                instructions=[],
                terminator=FallThrough(),
            )

            ctx.entry[fid] = mapping[node]

        # exit node is also noop, but stops control flow
        elif isinstance(node, FlowExit):
            ctx.nodes[mapping[node]] = Block(
                origin=fid,
                instructions=[],
                terminator=Emit(),
            )

            ctx.exit[fid] = mapping[node]

        # otherwise just callsite
        else:
            terminator = Emit() if not flow.edges.get(node) else FallThrough()
            ctx.nodes[mapping[node]] = lower_callsite(ctx, node, terminator)

    # wire edges
    for node, successors in flow.edges.items():
        ctx.edges[mapping[node]].extend([mapping[next] for next in successors])

    return mapping[flow.entry]


def lower_instance_or_snippet(
    ctx: LowLevelContext,
    target: Union[Instance, Snippet],
) -> List[Instruction]:
    out: List[Instruction] = []

    # placeholders
    instrs: List[InstructionId]
    operands: Dict[OperandId, Operand]

    # determine what we are lowering
    if isinstance(target, Snippet):
        operands = {}
        instrs = target.instructions
    else:
        operands = target.operands
        instrs = ctx.graph.basic.snippets.get(target.target).instructions

    # lower all instructions
    for iid in instrs:
        instr = ctx.graph.basic.instructions.get(iid)
        out.append(lower_instruction(ctx.graph, instr, operands))

    return out


def lower_callsite(
    ctx: LowLevelContext,
    cid: CallSiteId,
    terminator: Terminator,
) -> Block:
    instructions: List[Instruction] = []

    # retrieve callsite resolution
    resolution = ctx.graph.indices.resolution_by_callsite.get(cid)

    # we expected no ambiguity here
    assert len(resolution.accepted) == 1

    if isinstance(resolution.accepted[0].callable.target, SnippetId):
        instance = ctx.graph.indices.instance_by_callsite.get(cid)

        # append callsite specific bindings
        instructions.extend(lower_callsite_bindings(ctx, instance.bindings))

        # append instance instructions
        instructions.extend(lower_instance_or_snippet(ctx, instance))

    else:

        # append callsite specific bindings
        instructions.extend(lower_callsite_bindings(ctx, []))

    return Block(
        origin=cid,
        instructions=instructions,
        terminator=terminator,
    )
