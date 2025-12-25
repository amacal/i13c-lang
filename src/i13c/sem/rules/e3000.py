from typing import List

from i13c import diag, err
from i13c.sem.asm import INSTRUCTIONS_TABLE
from i13c.sem.nodes import Function, Instruction


def validate_assembly_mnemonic(functions: List[Function]) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if isinstance(stmt, Instruction):
                if stmt.mnemonic not in INSTRUCTIONS_TABLE:
                    diagnostics.append(err.report_e3000_unknown_instruction(stmt.ref))

    return diagnostics
