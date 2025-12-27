from typing import List, Set

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_duplicated_function_names(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    seen: Set[bytes] = set()

    for function in graph.functions.values():
        if function.identifier.name in seen:
            diagnostics.append(
                err.report_e3006_duplicated_function_names(
                    function.ref,
                    function.identifier.name,
                )
            )
        else:
            seen.add(function.identifier.name)

    return diagnostics
