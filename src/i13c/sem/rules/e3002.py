from typing import List

from i13c import diag, err
from i13c.sem import asm
from i13c.sem.graph import Graph


def validate_assembly_operand_types(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for instruction in graph.nodes.instructions.values():

        matched = False
        signature = asm.INSTRUCTIONS_TABLE.get(instruction.mnemonic.name)

        # unknown instruction mnemonic
        if signature is None:
            continue

        # early acceptance for instructions without operands
        if not instruction.operands and not signature.variants:
            continue

        # each possible variant has to be checked
        for variant in signature.variants:

            # check operand count
            if len(variant) != len(instruction.operands):
                continue

            # check each operand type
            for expected, operand in zip(variant, instruction.operands):
                if not isinstance(operand, expected):
                    break

            else:
                matched = True
                break

        # any match indicates success
        if not matched:
            diagnostics.append(
                err.report_e3002_invalid_operand_types(
                    instruction.ref,
                    [type(operand).__name__ for operand in instruction.operands],
                )
            )

    return diagnostics
