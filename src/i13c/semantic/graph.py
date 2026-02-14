from typing import Any, Dict

from i13c.core.dag import GraphGroup, GraphNode, Prefix
from i13c.semantic.model import (
    BasicNodes,
    CallGraph,
    IndexEdges,
    LiveComponents,
    SemanticGraph,
)
from i13c.semantic.nodes import configure_nodes
from i13c.semantic.rules import configure_rules
from i13c.semantic.syntax import SyntaxGraph


def configure_semantic_graph() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_nodes(),
            configure_rules(),
            configure_self(),
        ]
    )


def configure_self() -> GraphNode:
    return GraphNode(
        builder=build,
        produces=("semantic/graph",),
        requires=frozenset(
            {
                ("syntax", "syntax/graph"),
                ("entities", Prefix(value="entities/")),
                ("indices", Prefix(value="indices/")),
                ("resolutions", Prefix(value="resolutions/")),
                ("analyses", Prefix(value="analyses/")),
            }
        ),
    )


def build(
    syntax: SyntaxGraph,
    entities: Dict[str, Any],
    indices: Dict[str, Any],
    resolutions: Dict[str, Any],
    analyses: Dict[str, Any],
) -> SemanticGraph:
    return SemanticGraph(
        generator=syntax.generator,
        basic=BasicNodes(
            literals=entities["entities/literals"],
            operands=entities["entities/operands"],
            instructions=entities["entities/instructions"],
            expressions=entities["entities/expressions"],
            snippets=entities["entities/snippets"],
            functions=entities["entities/functions"],
            callsites=entities["entities/callsites"],
            parameters=entities["entities/parameters"],
            variables=entities["entities/variables"],
        ),
        indices=IndexEdges(
            terminality_by_function=indices["indices/terminality-by-function"],
            resolution_by_callsite=resolutions["resolutions/callsites"],
            resolution_by_instruction=resolutions["resolutions/instructions"],
            flowgraph_by_function=indices["indices/flowgraph-by-function"],
            instance_by_callsite=indices["indices/instance-by-callsite"],
            dataflow_by_flownode=indices["indices/dataflow-by-flownode"],
            variables_by_parameter=indices["indices/variables-by-parameter"],
            environment_by_flownode=indices["indices/environment-by-flownode"],
        ),
        callgraph=CallGraph(
            calls_by_caller=indices["indices/calls-by-caller"],
            calls_by_callee=indices["indices/calls-by-callee"],
        ),
        live=LiveComponents(
            entrypoints=indices["indices/entrypoints-by-callable"],
            flowgraph_by_function=analyses["analyses/flowgraph-by-function/live"],
        ),
        callable_live=analyses["analyses/callables/live"],
        callgraph_live=analyses["analyses/calls-by-caller/live"],
    )
