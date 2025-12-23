from typing import List, Set

from i13c import ast, diag, err


def validate_duplicated_parameter_names(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        # each function's parameters
        names: Set[bytes] = set()

        # asm and reg functions look similar enough
        for parameter in function.parameters:
            if parameter.name in names:
                diagnostics.append(
                    err.report_e3004_duplicated_parameter_names(
                        function.ref,
                        parameter.name,
                    )
                )
            else:
                names.add(parameter.name)

    return diagnostics
