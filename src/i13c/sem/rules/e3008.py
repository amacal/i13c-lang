from typing import List

from i13c import ast, diag, err, sym


def validate_called_symbol_exists(
    program: ast.Program,
    symbols: sym.SymbolTable,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        if isinstance(function, ast.RegFunction):
            for statement in function.statements:
                if statement.name not in symbols.entries:
                    diagnostics.append(
                        err.report_e3008_called_symbol_exists(
                            statement.ref,
                            statement.name,
                        )
                    )

    return diagnostics
