from typing import List

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.semantic.model import SemanticGraph


def configure_e3011() -> GraphNode:
    return GraphNode(
        builder=validate_entrypoint_exists,
        produces=("rules/e3011",),
        requires=frozenset({("graph", "semantic/graph")}),
    )


def validate_entrypoint_exists(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:

    if graph.live.entrypoints.size() > 0:
        return []

    return [err.report_e3011_missing_entrypoint_function()]
