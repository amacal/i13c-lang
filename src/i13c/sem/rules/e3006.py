from typing import List, Set

from i13c import ast, diag, err


def validate_duplicated_function_names(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    function_names: Set[bytes] = set()

    for function in program.functions:
        if function.name not in function_names:
            function_names.add(function.name)

        else:
            diagnostics.append(
                err.report_e3006_duplicated_function_names(
                    function.ref,
                    function.name,
                )
            )

    return diagnostics
