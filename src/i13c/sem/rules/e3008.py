from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_called_symbol_exists(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, resolution in graph.indices.resolution_by_callsite.items():
        if not resolution.accepted:

            # truly missing if there are no rejected resolutions either
            if not resolution.rejected:
                diagnostics.append(
                    err.report_e3008_called_symbol_missing(
                        graph.basic.callsites.get(cid).ref,
                        graph.basic.callsites.get(cid).callee.name,
                    )
                )

    return diagnostics
