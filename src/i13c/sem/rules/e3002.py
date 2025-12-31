from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_assembly_operand_types(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for iid, resolution in graph.instruction_resolutions.items():
        if not resolution.accepted and resolution.rejected:
            for rejection in resolution.rejected:
                diagnostics.append(
                    err.report_e3002_invalid_operand_types(
                        graph.instructions.get(iid).ref,
                        [str(spec) for spec in rejection.variant],
                    )
                )

    return diagnostics
