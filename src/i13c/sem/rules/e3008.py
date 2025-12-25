from typing import List

from i13c import diag, err
from i13c.sem.nodes import Call, Function


def validate_called_symbol_exists(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if isinstance(stmt, Call):
                if not stmt.candidates:
                    diagnostics.append(
                        err.report_e3008_called_symbol_exists(
                            stmt.ref,
                            stmt.name,
                        )
                    )

    return diagnostics
