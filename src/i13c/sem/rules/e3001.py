from typing import List

from i13c import ast, diag, err


def validate_immediate_out_of_range(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        if isinstance(function, ast.AsmFunction):
            for instruction in function.instructions:
                for operand in instruction.operands:
                    if isinstance(operand, ast.Immediate):
                        if not (0 <= operand.value <= 0xFFFFFFFFFFFFFFFF):
                            diagnostics.append(
                                err.report_e3001_immediate_out_of_range(
                                    instruction.ref,
                                    operand.value,
                                )
                            )

    return diagnostics
