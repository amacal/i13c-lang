from typing import Dict, List, Optional, Union

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.ir import FallThrough, Instruction, Stop, Terminator
from i13c.lowering.bind import lower_callsite_bindings
from i13c.lowering.graph import LowLevelGraph
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


def build_low_level_graph(graph: SemanticGraph) -> LowLevelGraph:
    entry: Optional[BlockId] = None
    nodes: Dict[BlockId, Block] = {}
    edges: Dict[BlockId, List[BlockId]] = {}

    for fid, flowgraph in graph.live.flowgraph_by_function.items():
        block = lower_function_flow(graph, nodes, edges, fid, flowgraph)

        if graph.live.entrypoints.contains(fid):
            entry = block

    if entry is None:
        for snid in graph.live.entrypoints.keys():
            assert isinstance(snid, SnippetId)
            entry = lower_snippet(graph, nodes, edges, snid)

    # entry has to be found
    assert entry is not None

    return LowLevelGraph(
        generator=graph.generator,
        entry=entry,
        nodes=OneToOne[BlockId, Block].instance(nodes),
        edges=OneToMany[BlockId, BlockId].instance(edges),
    )


def lower_snippet(
    graph: SemanticGraph,
    nodes: Dict[BlockId, Block],
    edges: Dict[BlockId, List[BlockId]],
    snid: SnippetId,
) -> BlockId:

    # create instructions for snippet
    bid = BlockId(value=graph.generator.next())
    snippet = graph.basic.snippets.get(snid)
    instrs = lower_instance_or_snippet(graph, snippet)

    # append to graph
    edges[bid] = []
    nodes[bid] = Block(origin=snid, instructions=instrs, terminator=Stop())

    return bid


def lower_function_flow(
    graph: SemanticGraph,
    nodes: Dict[BlockId, Block],
    edges: Dict[BlockId, List[BlockId]],
    fid: FunctionId,
    flow: FlowGraph,
) -> BlockId:
    mapping: Dict[FlowNode, BlockId] = {}
    generator: Generator = graph.generator

    # assign ID to each FlowNode
    for node in flow.nodes():
        mapping[node] = BlockId(value=generator.next())
        edges[mapping[node]] = []

    for node in flow.nodes():
        # entry node is noop just transfers control
        if isinstance(node, FlowEntry):
            nodes[mapping[node]] = Block(
                origin=fid,
                instructions=[],
                terminator=FallThrough(),
            )

        # exit node is also noop, but stops control flow
        elif isinstance(node, FlowExit):
            nodes[mapping[node]] = Block(
                origin=fid,
                instructions=[],
                terminator=Stop(),
            )

        # otherwise just callsite
        else:
            terminator = Stop() if not flow.edges.get(node) else FallThrough()
            nodes[mapping[node]] = lower_callsite(graph, node, terminator)

    # wire edges
    for node, successors in flow.edges.items():
        edges[mapping[node]].extend([mapping[next] for next in successors])

    return mapping[flow.entry]


def lower_instance_or_snippet(
    graph: SemanticGraph,
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
        instrs = graph.basic.snippets.get(target.target).instructions

    # lower all instructions
    for iid in instrs:
        instr = graph.basic.instructions.get(iid)
        out.append(lower_instruction(graph, instr, operands))

    return out


def lower_callsite(
    graph: SemanticGraph, cid: CallSiteId, terminator: Terminator
) -> Block:
    instructions: List[Instruction] = []

    # currently we call only instances
    instance = graph.indices.instance_by_callsite.get(cid)

    # append callsite specific bindings
    instructions.extend(lower_callsite_bindings(graph, instance.bindings))

    # append instance instructions
    instructions.extend(lower_instance_or_snippet(graph, instance))

    return Block(
        origin=cid,
        instructions=instructions,
        terminator=terminator,
    )
