from typing import List, Set

from i13c import ast, diag, err


def validate_duplicated_function_clobbers(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        # each function's clobbers
        seen: Set[bytes] = set()
        clobbers: List[ast.Register] = []

        if isinstance(function, ast.AsmFunction):
            clobbers = function.clobbers

        # asm functions will be the only ones with clobbers
        for clobber in clobbers:
            if clobber.name in seen:
                diagnostics.append(
                    err.report_e3005_duplicated_function_clobbers(
                        function.ref,
                        clobber.name,
                    )
                )
            else:
                seen.add(clobber.name)

    return diagnostics
