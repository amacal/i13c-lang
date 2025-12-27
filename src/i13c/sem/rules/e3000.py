from typing import List

from i13c import diag, err
from i13c.sem.asm import INSTRUCTIONS_TABLE
from i13c.sem.model import SemanticGraph


def validate_assembly_mnemonic(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for snippet in graph.snippets.values():
        for instruction in snippet.instructions:
            if instruction.mnemonic.name not in INSTRUCTIONS_TABLE:
                diagnostics.append(
                    err.report_e3000_unknown_instruction(instruction.ref)
                )

    return diagnostics
