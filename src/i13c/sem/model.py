from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from i13c.sem.asm import Instruction, InstructionId
from i13c.sem.asm import Resolution as InstructionResolution
from i13c.sem.asm import build_instructions
from i13c.sem.asm import build_resolutions as build_instruction_resolutions
from i13c.sem.callable import CallableTarget
from i13c.sem.callgraphs import build_callgraph
from i13c.sem.callsite import CallSite, CallSiteId, build_callsites
from i13c.sem.entrypoint import EntryPoint, build_entrypoints
from i13c.sem.flowgraphs import FlowGraph, build_flowgraphs
from i13c.sem.function import Function, FunctionId, build_functions
from i13c.sem.literal import Literal, LiteralId, build_literals
from i13c.sem.live import (
    build_callable_live,
    build_callgraph_live,
    build_flowgraphs_live,
)
from i13c.sem.resolve import Resolution as CallSiteResolution
from i13c.sem.resolve import build_resolutions as build_callsite_resolutions
from i13c.sem.snippet import Snippet, SnippetId, build_snippets
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.terminal import Terminality, build_terminalities


@dataclass(kw_only=True)
class SemanticGraph:
    entrypoints: List[EntryPoint]

    literals: Dict[LiteralId, Literal]
    snippets: Dict[SnippetId, Snippet]
    functions: Dict[FunctionId, Function]
    callsites: Dict[CallSiteId, CallSite]
    instructions: Dict[InstructionId, Instruction]

    callgraph: Dict[CallableTarget, List[Tuple[CallSiteId, CallableTarget]]]
    callgraph_live: Dict[CallableTarget, List[Tuple[CallSiteId, CallableTarget]]]
    callable_live: Set[CallableTarget]

    function_flowgraphs: Dict[FunctionId, FlowGraph]
    function_flowgraphs_live: Dict[FunctionId, FlowGraph]
    function_terminalities: Dict[FunctionId, Terminality]

    callsite_resolutions: Dict[CallSiteId, CallSiteResolution]
    instruction_resolutions: Dict[InstructionId, InstructionResolution]


def build_semantic_graph(graph: SyntaxGraph) -> SemanticGraph:
    literals = build_literals(graph)
    snippets = build_snippets(graph)
    functions = build_functions(graph)
    callsites = build_callsites(graph)
    instructions = build_instructions(graph)

    entrypoints = build_entrypoints(functions, snippets)
    function_flowgraphs = build_flowgraphs(functions)

    callsite_resolutions = build_callsite_resolutions(
        functions,
        snippets,
        callsites,
        literals,
    )

    callgraph = build_callgraph(snippets, functions, callsite_resolutions)
    instruction_resolutions = build_instruction_resolutions(instructions)

    function_terminalities = build_terminalities(
        snippets,
        functions,
        function_flowgraphs,
        callsite_resolutions,
    )

    callgraph_live = build_callgraph_live(
        entrypoints,
        snippets,
        function_flowgraphs,
        callgraph,
        function_terminalities,
        callsite_resolutions,
    )

    callable_live = build_callable_live(
        entrypoints,
        callgraph_live,
    )

    function_flowgraphs_live = build_flowgraphs_live(
        function_flowgraphs,
        callsite_resolutions,
        snippets,
        function_terminalities,
    )

    return SemanticGraph(
        entrypoints=entrypoints,
        literals=literals,
        snippets=snippets,
        functions=functions,
        callsites=callsites,
        callgraph=callgraph,
        callgraph_live=callgraph_live,
        callable_live=callable_live,
        instructions=instructions,
        function_flowgraphs=function_flowgraphs,
        function_flowgraphs_live=function_flowgraphs_live,
        function_terminalities=function_terminalities,
        callsite_resolutions=callsite_resolutions,
        instruction_resolutions=instruction_resolutions,
    )
