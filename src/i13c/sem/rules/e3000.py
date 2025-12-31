from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_assembly_mnemonic(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for iid, resolution in graph.resolution_by_instruction.items():
        if not resolution.accepted and not resolution.rejected:
            diagnostics.append(
                err.report_e3000_unknown_instruction(graph.instructions.get(iid).ref)
            )

    return diagnostics
