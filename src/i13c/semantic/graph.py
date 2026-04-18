from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, Prefix
from i13c.semantic.model import (
    CallGraph,
    IndexEdges,
    LiveComponents,
    SemanticGraph,
    SemanticRules,
)
from i13c.semantic.nodes import configure_nodes
from i13c.semantic.nodes.entities import parse_entities
from i13c.semantic.nodes.resolutions import parse_resolutions


def configure_e3xxx() -> GraphNode:
    def build(rules: Dict[str, List[Diagnostic]]) -> SemanticRules:
        return SemanticRules(data=rules)

    return GraphNode(
        builder=build,
        constraint=None,
        produces=("rules/semantic",),
        requires=frozenset({("rules", Prefix(value="rules/e3"))}),
    )


def configure_semantic_graph() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_nodes(),
            configure_self(),
            configure_e3xxx(),
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
        entities=parse_entities(entities),
        indices=IndexEdges(
            binds_by_slots=indices.get("indices/binds/slots"),
            environments_by_snippets=indices.get("indices/environments/snippets"),
            signatures_by_names=indices.get("indices/signatures/names"),
            dataflow_by_flownode=indices["indices/dataflow-by-flownode"],
            environment_by_flownode=indices["indices/environment-by-flownode"],
            flowgraph_by_function=indices["indices/flowgraph-by-function"],
            instance_by_callsite=indices.get("indices/instance-by-callsite"),
            resolution_by_callsite=resolutions["resolutions/callsites"],
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
        resolutions=parse_resolutions(resolutions),
    )
