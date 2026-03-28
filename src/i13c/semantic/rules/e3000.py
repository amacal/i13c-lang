from typing import List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from i13c.syntax.source import SpanLike


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
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for iid, resolution in resolutions.items():
        if not resolution.accepted and not resolution.rejected:
            diagnostics.append(
                report_e3000_unknown_instruction(instructions.get(iid).ref)
            )

    return diagnostics


def report_e3000_unknown_instruction(ref: SpanLike) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3000",
        message=f"Unknown instruction mnemonic at offset {ref.offset}",
    )
