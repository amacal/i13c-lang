from typing import List, Set

from i13c import diag, err
from i13c.sem.nodes import Function


def validate_duplicated_function_names(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    seen: Set[bytes] = set()

    for fn in functions:
        if fn.name in seen:
            diagnostics.append(
                err.report_e3006_duplicated_function_names(
                    fn.ref,
                    fn.name,
                )
            )
        else:
            seen.add(fn.name)

    return diagnostics
