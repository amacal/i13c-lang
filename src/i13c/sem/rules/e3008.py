from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_called_symbol_exists(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, resolution in graph.callsite_resolutions.items():
        if not resolution.accepted:
            diagnostics.append(
                err.report_e3008_called_symbol_missing(
                    graph.callsites[cid].ref,
                    graph.callsites[cid].callee.name,
                )
            )

    return diagnostics
