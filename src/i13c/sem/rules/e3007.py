from typing import List

from i13c import ast, diag, err


def validate_integer_literal_out_of_range(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        if isinstance(function, ast.RegFunction):
            for statement in function.statements:
                for argument in statement.arguments:
                    if not (0 <= argument.value <= 0xFFFFFFFFFFFFFFFF):
                        diagnostics.append(
                            err.report_e3007_integer_literal_out_of_range(
                                statement.ref,
                                argument.value,
                            )
                        )

    return diagnostics
