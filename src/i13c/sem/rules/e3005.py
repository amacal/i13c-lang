from typing import List, Set

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_duplicated_snippet_clobbers(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for snippet in graph.snippets.values():
        seen: Set[bytes] = set()

        for reg in snippet.clobbers:
            if reg.name in seen:
                diagnostics.append(
                    err.report_e3005_duplicated_snippet_clobbers(
                        snippet.ref,
                        reg.name,
                    )
                )
            else:
                seen.add(reg.name)

    return diagnostics
