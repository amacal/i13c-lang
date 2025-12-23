from typing import List

from i13c import ast, diag, err, sym


def validate_called_symbol_is_asm(
    program: ast.Program,
    symbols: sym.SymbolTable,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        if isinstance(function, ast.RegFunction):
            for statement in function.statements:
                if symbol := symbols.entries.get(statement.name):
                    if symbol.target.kind != sym.FUNCTION_KIND_ASM:
                        diagnostics.append(
                            err.report_e3009_called_symbol_is_asm(
                                statement.ref,
                                statement.name,
                            )
                        )

    return diagnostics
