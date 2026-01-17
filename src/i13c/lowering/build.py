from typing import Dict, List, Optional, Set, Union

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.bind import lower_callsite_bindings
from i13c.lowering.graph import LowLevelContext, LowLevelGraph
from i13c.lowering.instructions import lower_instruction
from i13c.lowering.linear import build_instruction_flow
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId, CallFlow, Flow
from i13c.lowering.typing.instructions import Call, Instruction, Label
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    FallThroughTerminator,
    Terminator,
    TrapTerminator,
)
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
        flows={},
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

    # entry has to be found
    assert entry is not None

    # patch function calls
    for block in ctx.nodes.values():

        # only callsite blocks may have calls
        if not isinstance(block.origin, CallSiteId):
            continue

        # patch all calls within block
        for idx, instr in enumerate(block.instructions):
            if isinstance(instr, CallFlow):
                block.instructions[idx] = Call(target=ctx.entry[instr.target])

    # emit entry first
    ctx.flows[entry] = build_instruction_flow(ctx, entry)

    # emit all other functions
    for fid in ctx.entry.keys():
        if ctx.entry[fid] != entry:
            ctx.flows[ctx.entry[fid]] = build_instruction_flow(ctx, ctx.entry[fid])

    # collect active labels
    active: Set[int] = {
        instr.target.value
        for flow in ctx.flows.values()
        for instr in flow
        if isinstance(instr, Call)
    }

    # remove inactive labels
    for fid in ctx.flows.keys():
        ctx.flows[fid] = [
            instr
            for instr in ctx.flows[fid]
            if not isinstance(instr, Label) or instr.id.value in active
        ]

    return LowLevelGraph(
        generator=graph.generator,
        entry=entry,
        nodes=OneToOne[BlockId, Block].instance(ctx.nodes),
        edges=OneToMany[BlockId, BlockId].instance(ctx.edges),
        flows=OneToMany[BlockId, Instruction].instance(ctx.flows),
    )


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

        # otherwise just callsite emitting either fallthrough or stop
        else:
            terminator = (
                FallThroughTerminator() if flow.edges.get(node) else TrapTerminator()
            )
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
    instructions: List[Union[Instruction, Flow]] = []

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

        # append callsite call instructions
        instructions.extend([CallFlow(target=resolution.accepted[0].callable.target)])

    return Block(
        origin=cid,
        instructions=instructions,
        terminator=terminator,
    )
