from typing import List

from i13c import ast, diag, err
from i13c.sem.asm import INSTRUCTIONS_TABLE


def validate_assembly_mnemonic(
    program: ast.Program,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        if isinstance(function, ast.AsmFunction):
            for instruction in function.instructions:

                if instruction.mnemonic.name not in INSTRUCTIONS_TABLE:
                    diagnostics.append(
                        err.report_e3000_unknown_instruction(
                            instruction.ref,
                        )
                    )

    return diagnostics
