from typing import List

from i13c import diag, err
from i13c.sem.nodes import Function, Immediate, Instruction


def validate_immediate_out_of_range(functions: List[Function]) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if isinstance(stmt, Instruction):
                for operand in stmt.operands:
                    if isinstance(operand, Immediate):
                        if not (0 <= operand.value <= 0xFFFFFFFFFFFFFFFF):
                            diagnostics.append(
                                err.report_e3001_immediate_out_of_range(
                                    stmt.ref,
                                    operand.value,
                                )
                            )

    return diagnostics
