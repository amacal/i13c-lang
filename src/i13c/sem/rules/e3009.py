from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_called_symbol_is_snippet(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, resolution in graph.indices.resolution_by_callsite.items():
        for acceptance in resolution.accepted:
            if acceptance.callable.kind != b"snippet":
                diagnostics.append(
                    err.report_e3009_called_symbol_is_not_a_snippet(
                        graph.basic.callsites.get(cid).ref,
                        graph.basic.callsites.get(cid).callee.name,
                    )
                )

    return diagnostics
