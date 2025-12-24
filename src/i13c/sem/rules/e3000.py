from typing import List

from i13c import diag, err
from i13c.sem import asm, rel


def validate_assembly_mnemonic(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for instruction in relationships.nodes.instructions.values():

        # absence means unknown instruction
        if instruction.mnemonic.name not in asm.INSTRUCTIONS_TABLE:
            diagnostics.append(
                err.report_e3000_unknown_instruction(
                    instruction.ref,
                )
            )

    return diagnostics
