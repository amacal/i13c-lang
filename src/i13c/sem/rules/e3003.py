from typing import List, Set

from i13c import ast, diag, err


def validate_duplicated_parameter_bindings(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        # each function's bindings
        bindings: Set[bytes] = set()
        parameters: List[ast.AsmParameter] = []

        if isinstance(function, ast.AsmFunction):
            parameters = function.parameters

        # asm functions will be the only ones with parameter bindings
        for parameter in parameters:
            if parameter.bind.name in bindings:
                diagnostics.append(
                    err.report_e3003_duplicated_parameter_bindings(
                        function.ref,
                        parameter.bind.name,
                    )
                )
            else:
                bindings.add(parameter.bind.name)

    return diagnostics
