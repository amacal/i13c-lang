from typing import List

from i13c import diag, err
from i13c.sem.asm import INSTRUCTIONS_TABLE
from i13c.sem.nodes import Function, Instruction


def validate_assembly_operand_types(functions: List[Function]) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if not isinstance(stmt, Instruction):
                continue

            # unknown mnemonic handled elsewhere
            sig = INSTRUCTIONS_TABLE.get(stmt.mnemonic)
            if sig is None:
                continue

            # no operands expected
            if not stmt.operands and not sig.variants:
                continue

            # final outcome
            matched = False

            for variant in sig.variants:
                if len(variant) != len(stmt.operands):
                    continue

                # check each operand type
                for expected, operand in zip(variant, stmt.operands):
                    if not isinstance(operand, expected):
                        break

                # report success
                else:
                    matched = True
                    break

            # report failure
            if not matched:
                diagnostics.append(
                    err.report_e3002_invalid_operand_types(
                        stmt.ref,
                        [type(op).__name__ for op in stmt.operands],
                    )
                )

    return diagnostics
