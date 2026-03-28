from typing import List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from i13c.syntax.source import SpanLike


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
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for iid, resolution in resolutions.items():
        if not resolution.accepted and resolution.rejected:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_e3002_invalid_operand_types(
                        instructions.get(iid).ref,
                        [str(spec) for spec in rejection.variant],
                    )
                )

    return diagnostics


def report_e3002_invalid_operand_types(ref: SpanLike, found: List[str]) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3002",
        message=f"Invalid operand types ({', '.join(found)}) at offset {ref.offset}",
    )
