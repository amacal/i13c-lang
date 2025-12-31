from dataclasses import dataclass
from typing import Dict, List, Set

from i13c.sem.asm import Instruction, InstructionId
from i13c.sem.asm import Resolution as InstructionResolution
from i13c.sem.asm import build_instructions
from i13c.sem.asm import build_resolutions as build_resolution_by_instruction
from i13c.sem.callable import CallableTarget
from i13c.sem.callgraphs import CallPair, build_callgraph
from i13c.sem.callsite import CallSite, CallSiteId, build_callsites
from i13c.sem.entrypoint import EntryPoint, build_entrypoints
from i13c.sem.flowgraphs import FlowGraph, build_flowgraphs
from i13c.sem.function import Function, FunctionId, build_functions
from i13c.sem.infra import OneToMany, OneToOne
from i13c.sem.literal import Literal, LiteralId, build_literals
from i13c.sem.live import (
    build_callable_live,
    build_callgraph_live,
    build_flowgraphs_live,
)
from i13c.sem.resolve import Resolution as CallSiteResolution
from i13c.sem.resolve import build_resolutions as build_resolution_by_callsite
from i13c.sem.snippet import Snippet, SnippetId, build_snippets
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.terminal import Terminality, build_terminalities


@dataclass
class BasicNodes:
    literals: OneToOne[LiteralId, Literal]
    instructions: OneToOne[InstructionId, Instruction]
    snippets: OneToOne[SnippetId, Snippet]
    functions: OneToOne[FunctionId, Function]
    callsites: OneToOne[CallSiteId, CallSite]


@dataclass
class IndexEdges:
    terminality_by_function: OneToOne[FunctionId, Terminality]
    resolution_by_callsite: OneToOne[CallSiteId, CallSiteResolution]
    resolution_by_instruction: OneToOne[InstructionId, InstructionResolution]
    flowgraph_by_function: OneToOne[FunctionId, FlowGraph]


@dataclass
class LiveComponents:
    entrypoints: OneToOne[CallableTarget, EntryPoint]
    flowgraph_by_function: OneToOne[FunctionId, FlowGraph]


@dataclass
class CallGraph:
    calls_by_caller: OneToMany[CallableTarget, CallPair]
    calls_by_callee: OneToMany[CallableTarget, CallPair]


@dataclass(kw_only=True)
class SemanticGraph:
    callgraph_live: Dict[CallableTarget, List[CallPair]]
    callable_live: Set[CallableTarget]

    basic: BasicNodes
    indices: IndexEdges
    callgraph: CallGraph
    live: LiveComponents


def build_semantic_graph(graph: SyntaxGraph) -> SemanticGraph:
    literals = build_literals(graph)
    snippets = build_snippets(graph)
    functions = build_functions(graph)
    callsites = build_callsites(graph)
    instructions = build_instructions(graph)

    flowgraph_by_function = build_flowgraphs(functions)

    resolution_by_callsite = build_resolution_by_callsite(
        functions,
        snippets,
        callsites,
        literals,
    )

    callgraph, by_callee = build_callgraph(snippets, functions, resolution_by_callsite)
    resolution_by_instruction = build_resolution_by_instruction(instructions)

    terminality_by_function = build_terminalities(
        snippets,
        functions,
        flowgraph_by_function,
        resolution_by_callsite,
    )

    entrypoints = build_entrypoints(
        functions,
        snippets,
        terminality_by_function,
    )

    flowgraph_by_function_live = build_flowgraphs_live(
        flowgraph_by_function,
        resolution_by_callsite,
        snippets,
        terminality_by_function,
    )

    callgraph_live = build_callgraph_live(flowgraph_by_function_live, callgraph)

    callable_live = build_callable_live(
        entrypoints,
        callgraph_live,
    )

    return SemanticGraph(
        basic=BasicNodes(
            literals=OneToOne[LiteralId, Literal].instance(literals),
            instructions=OneToOne[InstructionId, Instruction].instance(instructions),
            snippets=OneToOne[SnippetId, Snippet].instance(snippets),
            functions=OneToOne[FunctionId, Function].instance(functions),
            callsites=OneToOne[CallSiteId, CallSite].instance(callsites),
        ),
        indices=IndexEdges(
            terminality_by_function=OneToOne[FunctionId, Terminality].instance(
                terminality_by_function
            ),
            resolution_by_callsite=OneToOne[CallSiteId, CallSiteResolution].instance(
                resolution_by_callsite
            ),
            resolution_by_instruction=OneToOne[
                InstructionId, InstructionResolution
            ].instance(resolution_by_instruction),
            flowgraph_by_function=OneToOne[FunctionId, FlowGraph].instance(
                flowgraph_by_function
            ),
        ),
        callgraph=CallGraph(
            calls_by_caller=OneToMany[CallableTarget, CallPair].instance(callgraph),
            calls_by_callee=OneToMany[CallableTarget, CallPair].instance(by_callee),
        ),
        live=LiveComponents(
            entrypoints=OneToOne[CallableTarget, EntryPoint].instance(entrypoints),
            flowgraph_by_function=OneToOne[FunctionId, FlowGraph].instance(
                flowgraph_by_function_live
            ),
        ),
        callgraph_live=callgraph_live,
        callable_live=callable_live,
    )
