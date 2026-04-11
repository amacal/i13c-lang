from typing import Any, Dict

from i13c.core.graph import GraphGroup, GraphNode, Prefix
from i13c.semantic.model import (
    BasicNodes,
    CallGraph,
    IndexEdges,
    LiveComponents,
    ResolutionNodes,
    SemanticGraph,
)
from i13c.semantic.nodes import configure_nodes
from i13c.semantic.rules import configure_rules


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
        constraint=None,
        produces=("semantic/graph",),
        requires=frozenset(
            {
                ("syntax", "syntax/graph"),
                ("rules", "rules/semantic"),
                ("entities", Prefix(value="entities/")),
                ("indices", Prefix(value="indices/")),
                ("resolutions", Prefix(value="resolutions/")),
                ("analyses", Prefix(value="analyses/")),
            }
        ),
    )


def build(
    entities: Dict[str, Any],
    indices: Dict[str, Any],
    resolutions: Dict[str, Any],
    analyses: Dict[str, Any],
    **kwargs: Dict[str, Any],
) -> SemanticGraph:
    return SemanticGraph(
        basic=BasicNodes(
            bindings=entities["entities/bindings"],
            binds=entities["entities/binds"],
            callsites=entities["entities/callsites"],
            expressions=entities["entities/expressions"],
            functions=entities["entities/functions"],
            instructions=entities["entities/instructions"],
            literals=entities["entities/literals"],
            operands=entities["entities/operands"],
            parameters=entities["entities/parameters"],
            ranges=entities["entities/ranges"],
            snippets=entities["entities/snippets"],
            types=entities["entities/types"],
            usages=entities["entities/usages"],
            values=entities["entities/values"],
            variables=entities["entities/variables"],
        ),
        indices=IndexEdges(
            dataflow_by_flownode=indices["indices/dataflow-by-flownode"],
            environment_by_flownode=indices["indices/environment-by-flownode"],
            flowgraph_by_function=indices["indices/flowgraph-by-function"],
            instance_by_callsite=indices["indices/instance-by-callsite"],
            resolution_by_callsite=resolutions["resolutions/callsites"],
            resolution_by_instruction=resolutions["resolutions/instructions"],
            resolution_by_value=resolutions["resolutions/values"],
            terminality_by_function=indices["indices/terminality-by-function"],
            usages_by_expression=indices["indices/usages-by-expression"],
            variables_by_parameter=indices["indices/variables-by-source"],
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
        resolutions=ResolutionNodes(
            binds=resolutions.get("resolutions/binds"),
            ranges=resolutions.get("resolutions/ranges"),
            types=resolutions.get("resolutions/types"),
        ),
    )
