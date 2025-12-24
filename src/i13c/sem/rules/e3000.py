from typing import List

from i13c import diag, err
from i13c.sem import asm
from i13c.sem.graph import Graph


def validate_assembly_mnemonic(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for instruction in graph.nodes.instructions.values():

        # absence means unknown instruction
        if instruction.mnemonic.name not in asm.INSTRUCTIONS_TABLE:
            diagnostics.append(
                err.report_e3000_unknown_instruction(
                    instruction.ref,
                )
            )

    return diagnostics
