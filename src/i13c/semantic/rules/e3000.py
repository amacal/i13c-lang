from typing import List

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.resolutions.instructions import InstructionResolution


def configure_e3000() -> GraphNode:
    return GraphNode(
        builder=validate_assembly_mnemonic,
        constraint=None,
        produces=("rules/e3000",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("resolutions", "resolutions/instructions"),
            }
        ),
    )


def validate_assembly_mnemonic(
    instructions: OneToOne[InstructionId, Instruction],
    resolutions: OneToOne[InstructionId, InstructionResolution],
) -> List[diagnostics.Diagnostic]:
    diagnostics: List[diagnostics.Diagnostic] = []

    for iid, resolution in resolutions.items():
        if not resolution.accepted and not resolution.rejected:
            diagnostics.append(
                err.report_e3000_unknown_instruction(instructions.get(iid).ref)
            )

    return diagnostics
