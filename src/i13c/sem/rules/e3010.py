from typing import List, Optional

from i13c import ast, diag, err, sym


def validate_called_symbol_termination(
    program: ast.Program,
    symbols: sym.SymbolTable,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        if function.terminal:
            if isinstance(function, ast.RegFunction):
                terminal = False
                matched: Optional[ast.CallStatement] = None

                # find for last called symbol
                for statement in function.statements:
                    if symbol := symbols.entries.get(statement.name):
                        (matched, terminal) = statement, symbol.target.terminal

                if matched and not terminal:
                    diagnostics.append(
                        err.report_e3010_callee_is_non_terminal(
                            matched.ref,
                            matched.name,
                        )
                    )

    return diagnostics
