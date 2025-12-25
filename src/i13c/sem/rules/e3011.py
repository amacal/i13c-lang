from typing import List

from i13c import diag, err
from i13c.sem.nodes import Call, Function


def validate_called_arguments_count(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if not isinstance(stmt, Call):
                continue

            # snapshot before filtering
            before = list(stmt.candidates)

            # keep only functions with matching arity
            stmt.candidates = [
                fn
                for fn in stmt.candidates
                if len(fn.parameters) == len(stmt.arguments)
            ]

            # name matched but arity eliminated all
            if before and not stmt.candidates:
                diagnostics.append(
                    err.report_e3011_called_argument_count_mismatch(
                        stmt.ref,
                        expected=len(before[0].parameters),
                        found=len(stmt.arguments),
                    )
                )

    return diagnostics
