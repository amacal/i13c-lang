from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_assembly_operand_types(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for iid, resolution in graph.indices.resolution_by_instruction.items():
        if not resolution.accepted and resolution.rejected:
            for rejection in resolution.rejected:
                diagnostics.append(
                    err.report_e3002_invalid_operand_types(
                        graph.basic.instructions.get(iid).ref,
                        [str(spec) for spec in rejection.variant],
                    )
                )

    return diagnostics
