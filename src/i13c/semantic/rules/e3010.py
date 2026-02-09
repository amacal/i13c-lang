from typing import List

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.semantic.model import SemanticGraph


def configure_e3010() -> GraphNode:
    return GraphNode(
        builder=validate_called_symbol_terminality,
        produces=("rules/e3010",),
        requires=frozenset({("graph", "semantic/graph")}),
    )


def validate_called_symbol_terminality(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, terminality in graph.indices.terminality_by_function.items():
        # we need to compare against the function definition
        function = graph.basic.functions.get(fid)

        # if the terminality expectations do not match, report an error
        if function.noreturn != terminality.noreturn:
            diagnostics.append(
                err.report_e3010_function_has_wrong_terminality(
                    function.ref,
                    function.identifier.name,
                )
            )

    return diagnostics
