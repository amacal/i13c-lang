from typing import List

from i13c import diag, err
from i13c.sem.nodes import Call, Function


def validate_called_symbol_termination(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        if not fn.noreturn or fn.kind in ["snippet"]:
            continue

        for exit_point in fn.exit_points:
            # implicitly non-terminal
            if not exit_point.statement or not isinstance(exit_point.statement, Call):
                diagnostics.append(
                    err.report_e3010_callee_is_non_terminal(
                        fn.ref,
                        fn.name,
                    )
                )

                break

            # complain on any non-terminal callee
            for callee in exit_point.statement.candidates:
                if not callee.noreturn:
                    diagnostics.append(
                        err.report_e3010_callee_is_non_terminal(
                            exit_point.statement.ref,
                            exit_point.statement.name,
                        )
                    )

                    break

    return diagnostics
