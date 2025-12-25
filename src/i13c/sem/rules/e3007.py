from typing import List

from i13c import diag, err
from i13c.sem.nodes import Call, Function


def validate_integer_literal_out_of_range(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if isinstance(stmt, Call):
                for arg in stmt.arguments:
                    if not (0 <= arg.value.value <= 0xFFFFFFFFFFFFFFFF):
                        diagnostics.append(
                            err.report_e3007_integer_literal_out_of_range(
                                arg.ref,
                                arg.value.value,
                            )
                        )

    return diagnostics
