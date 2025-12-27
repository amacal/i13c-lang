from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_called_symbol_is_snippet(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, resolution in graph.callsite_resolutions.items():
        for acceptance in resolution.accepted:
            if acceptance.callable.kind != b"snippet":
                diagnostics.append(
                    err.report_e3009_called_symbol_is_not_a_snippet(
                        graph.callsites[cid].ref,
                        graph.callsites[cid].callee.name,
                    )
                )

    return diagnostics
