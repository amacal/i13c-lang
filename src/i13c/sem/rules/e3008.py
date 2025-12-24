from typing import List

from i13c import diag, err
from i13c.sem.analysis import Analysis
from i13c.sem.graph import Graph


def validate_called_symbol_exists(
    graph: Graph,
    analysis: Analysis,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in graph.nodes.calls.id_to_node.items():
        if cid not in graph.edges.call_targets.keys():
            diagnostics.append(
                err.report_e3008_called_symbol_exists(
                    call.ref,
                    call.name,
                )
            )

    return diagnostics
