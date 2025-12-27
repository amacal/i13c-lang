from dataclasses import dataclass
from typing import Dict

from i13c.sem.asm import InstructionId, InstructionResolution
from i13c.sem.callsite import CallSite, CallSiteId, build_callsites
from i13c.sem.flows import FlowGraph, build_flowgraphs
from i13c.sem.function import Function, FunctionId, build_functions
from i13c.sem.literal import Literal, LiteralId, build_literals
from i13c.sem.resolve import Resolution, build_resolutions
from i13c.sem.snippet import Snippet, SnippetId, build_snippets
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.terminal import Terminality, build_terminalities


@dataclass(kw_only=True)
class SemanticGraph:
    literals: Dict[LiteralId, Literal]
    snippets: Dict[SnippetId, Snippet]
    functions: Dict[FunctionId, Function]
    callsites: Dict[CallSiteId, CallSite]

    function_flowgraphs: Dict[FunctionId, FlowGraph]
    function_terminalities: Dict[FunctionId, Terminality]

    callsite_resolutions: Dict[CallSiteId, Resolution]
    instruction_resolutions: Dict[InstructionId, InstructionResolution]


def build_semantic_graph(graph: SyntaxGraph) -> SemanticGraph:
    literals = build_literals(graph)
    snippets = build_snippets(graph)
    functions = build_functions(graph)
    callsites = build_callsites(graph)
    function_flowgraphs = build_flowgraphs(functions)
    callsite_resolutions = build_resolutions(
        functions,
        snippets,
        callsites,
        literals,
    )

    function_terminalities = build_terminalities(
        snippets,
        functions,
        function_flowgraphs,
        callsite_resolutions,
    )

    return SemanticGraph(
        literals=literals,
        snippets=snippets,
        functions=functions,
        callsites=callsites,
        function_flowgraphs=function_flowgraphs,
        callsite_resolutions=callsite_resolutions,
        function_terminalities=function_terminalities,
        instruction_resolutions={},
    )
