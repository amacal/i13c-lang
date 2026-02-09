from typing import List

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.semantic.model import SemanticGraph


def configure_e3012() -> GraphNode:
    return GraphNode(
        builder=validate_entrypoint_is_single,
        produces=("rules/e3012",),
        requires=frozenset({("graph", "semantic/graph")}),
    )


def validate_entrypoint_is_single(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:

    if graph.live.entrypoints.size() <= 1:
        return []

    return [err.report_e3012_multiple_entrypoint_functions()]
