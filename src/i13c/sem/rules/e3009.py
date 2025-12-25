from typing import List

from i13c import diag, err
from i13c.sem.nodes import Call, Function, Instruction


def validate_called_symbol_is_snippet(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if not isinstance(stmt, Call):
                continue

            for callee in stmt.candidates:
                # a snippet is a function whose body contains Instructions
                is_snippet = any(isinstance(x, Instruction) for x in callee.body)

                if not is_snippet:
                    diagnostics.append(
                        err.report_e3009_called_symbol_is_not_a_snippet(
                            stmt.ref,
                            stmt.name,
                        )
                    )

    return diagnostics
