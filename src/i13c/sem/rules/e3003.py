from typing import List, Set

from i13c import diag, err
from i13c.sem.nodes import Function


def validate_duplicated_slot_bindings(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        seen: Set[bytes] = set()

        for param in fn.parameters:
            if param.bind is None:
                continue

            if param.bind.name in seen:
                diagnostics.append(
                    err.report_e3003_duplicated_slot_bindings(
                        fn.ref,
                        param.bind.name,
                    )
                )
            else:
                seen.add(param.bind.name)

    return diagnostics
