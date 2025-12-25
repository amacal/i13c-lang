from typing import List, Set

from i13c import diag, err
from i13c.sem.nodes import Function


def validate_duplicated_snippet_clobbers(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        seen: Set[bytes] = set()

        for reg in fn.clobbers:
            if reg.name in seen:
                diagnostics.append(
                    err.report_e3005_duplicated_snippet_clobbers(
                        fn.ref,
                        reg.name,
                    )
                )
            else:
                seen.add(reg.name)

    return diagnostics
