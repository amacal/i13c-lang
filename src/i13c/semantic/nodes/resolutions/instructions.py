from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.operands import OperandId
from i13c.semantic.typing.resolutions.instructions import (
    InstructionAcceptance,
    InstructionRejection,
    InstructionResolution,
    MnemonicVariant,
    OperandSpec,
)
from i13c.semantic.typing.resolutions.operands import OperandAcceptance

INSTRUCTIONS_TABLE: Dict[bytes, List[MnemonicVariant]] = {
    b"add": [
        (OperandSpec.reg64(), OperandSpec.imm8()),
        (OperandSpec.reg64(), OperandSpec.imm16()),
        (OperandSpec.reg64(), OperandSpec.imm32()),
        (OperandSpec.reg64(), OperandSpec.reg64()),
        (OperandSpec.reg32(), OperandSpec.imm32()),
    ],
    b"bswap": [
        (OperandSpec.reg32(),),
        (OperandSpec.reg64(),),
    ],
    b"lea": [
        (OperandSpec.reg32(), OperandSpec.addr()),
        (OperandSpec.reg64(), OperandSpec.addr()),
    ],
    b"mov": [
        (OperandSpec.reg64(), OperandSpec.imm8()),
        (OperandSpec.reg64(), OperandSpec.imm16()),
        (OperandSpec.reg64(), OperandSpec.imm32()),
        (OperandSpec.reg64(), OperandSpec.imm64()),
        (OperandSpec.reg64(), OperandSpec.reg64()),
        (OperandSpec.reg64(), OperandSpec.addr()),
        (OperandSpec.reg32(), OperandSpec.imm8()),
        (OperandSpec.reg32(), OperandSpec.imm16()),
        (OperandSpec.reg32(), OperandSpec.imm32()),
        (OperandSpec.reg32(), OperandSpec.addr()),
        (OperandSpec.addr(), OperandSpec.imm8()),
        (OperandSpec.addr(), OperandSpec.imm16()),
        (OperandSpec.addr(), OperandSpec.imm32()),
        (OperandSpec.addr(), OperandSpec.reg64()),
    ],
    b"shl": [
        (OperandSpec.reg8(), OperandSpec.imm8()),
        (OperandSpec.reg16(), OperandSpec.imm8()),
        (OperandSpec.reg32(), OperandSpec.imm8()),
        (OperandSpec.reg64(), OperandSpec.imm8()),
        (OperandSpec.reg64(), OperandSpec.reg8(b"cl")),
    ],
    b"syscall": [()],
}


def configure_instruction_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_instruction_resolution,
        constraint=None,
        produces=("resolutions/instructions",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("operands", "resolutions/operands/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_instruction_resolution_e3023,
        constraint=None,
        produces=("rules/e3023",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("resolutions", "resolutions/instructions"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_instruction_resolution_accepted,
        constraint=check_instruction_resolution_accepted,
        produces=("resolutions/instructions/accepted",),
        requires=frozenset(
            {
                ("rule_e3023", "rules/e3023"),
                ("resolutions", "resolutions/instructions"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_instruction_resolution(
    instructions: OneToOne[InstructionId, Instruction],
    operands: OneToOne[OperandId, OperandAcceptance],
) -> OneToOne[InstructionId, InstructionResolution]:
    resolutions: Dict[InstructionId, InstructionResolution] = {}

    for iid, entry in instructions.items():
        resolution = InstructionResolution(
            accepted=[],
            rejected=[],
        )

        if entry.mnemonic.name not in INSTRUCTIONS_TABLE:
            resolution.rejected.append(
                InstructionRejection(
                    ref=entry.ref,
                    reason="unknown-mnemonic",
                )
            )

            continue

        for variant in INSTRUCTIONS_TABLE[entry.mnemonic.name]:
            collected: List[OperandAcceptance] = []

            if len(variant) != len(entry.operands):
                resolution.rejected.append(
                    InstructionRejection(
                        ref=entry.ref,
                        reason="arity-mismatch",
                    )
                )

            for spec, op in zip(variant, entry.operands):
                accepted = operands.get(op)

                if accepted.symbol != spec.symbol:
                    resolution.rejected.append(
                        InstructionRejection(
                            ref=entry.ref,
                            reason="width-mismatch",
                        )
                    )

                else:
                    collected.append(accepted)

            if len(variant) == len(collected):
                resolution.accepted.append(
                    InstructionAcceptance(
                        ref=entry.ref,
                        id=iid,
                        mnemonic=entry.mnemonic,
                        operands=tuple(collected),
                        variant=variant,
                    )
                )

        resolutions[iid] = resolution

    return OneToOne[InstructionId, InstructionResolution].instance(resolutions)


def check_instruction_resolution_accepted(
    rule_e3023: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3023) == 0


def build_instruction_resolution_accepted(
    resolutions: OneToOne[InstructionId, InstructionResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[InstructionId, InstructionAcceptance]:
    accepted: Dict[InstructionId, InstructionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[InstructionId, InstructionAcceptance].instance(accepted)


def validate_instruction_resolution_e3023(
    instructions: OneToOne[InstructionId, Instruction],
    resolutions: OneToOne[InstructionId, InstructionResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_instruction_resolution_e3023(instructions.get(id), rejection)
                )

    return diagnostics


def report_instruction_resolution_e3023(
    entry: Instruction, rejection: InstructionRejection
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3023",
        message=f"Invalid instruction {str(entry)}, reason: {rejection.reason}.",
    )
