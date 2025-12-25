from typing import List, Set

from i13c import diag, err
from i13c.sem.nodes import Function


def validate_duplicated_parameter_names(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        seen: Set[bytes] = set()

        for param in fn.parameters:
            if param.name in seen:
                diagnostics.append(
                    err.report_e3004_duplicated_parameter_names(fn.ref, param.name)
                )
            else:
                seen.add(param.name)

    return diagnostics
