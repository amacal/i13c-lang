from typing import List

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.resolutions.instructions import InstructionResolution


def configure_e3002() -> GraphNode:
    return GraphNode(
        builder=validate_assembly_operand_types,
        constraint=None,
        produces=("rules/e3002",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("resolutions", "resolutions/instructions"),
            }
        ),
    )


def validate_assembly_operand_types(
    instructions: OneToOne[InstructionId, Instruction],
    resolutions: OneToOne[InstructionId, InstructionResolution],
) -> List[diagnostics.Diagnostic]:
    diagnostics: List[diagnostics.Diagnostic] = []

    for iid, resolution in resolutions.items():
        if not resolution.accepted and resolution.rejected:
            for rejection in resolution.rejected:
                diagnostics.append(
                    err.report_e3002_invalid_operand_types(
                        instructions.get(iid).ref,
                        [str(spec) for spec in rejection.variant],
                    )
                )

    return diagnostics
