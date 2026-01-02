from typing import Dict, List, Optional, Tuple

from i13c.sem.infra import Configuration, OneToOne
from i13c.sem.typing.entities.instructions import Instruction, InstructionId
from i13c.sem.typing.entities.operands import Immediate, Operand, OperandId, Register
from i13c.sem.typing.resolutions.instructions import (
    InstructionAcceptance,
    InstructionRejection,
    InstructionRejectionReason,
    InstructionResolution,
    MnemonicBindings,
    MnemonicVariant,
    OperandSpec,
)
from i13c.sem.typing.resolutions.operands import OperandResolution


def configure_resolution_by_instruction() -> Configuration:
    return Configuration(
        builder=build_resolution_by_instruction,
        produces=("resolutions/instructions",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("operands", "entities/operands"),
                ("resolution_by_operand", "resolutions/operands"),
            }
        ),
    )


INSTRUCTIONS_TABLE: Dict[bytes, List[MnemonicVariant]] = {
    b"syscall": [()],
    b"mov": [
        (OperandSpec.register(), OperandSpec.immediate(64)),
        (OperandSpec.register(), OperandSpec.immediate(32)),
        (OperandSpec.register(), OperandSpec.immediate(16)),
        (OperandSpec.register(), OperandSpec.immediate(8)),
    ],
    b"shl": [
        (OperandSpec.register(), OperandSpec.immediate(8)),
    ],
}


def match_operand(
    operand: Operand, spec: OperandSpec
) -> Optional[InstructionRejectionReason]:

    if operand.kind != spec.kind:
        return b"type-mismatch"

    if operand.kind == b"register":
        assert isinstance(operand.target, Register)

        if spec.width != 64:
            return b"width-mismatch"

    if operand.kind == b"immediate":
        assert isinstance(operand.target, Immediate)

        if operand.target.width != spec.width:
            return b"width-mismatch"

    return None


def match_instruction(
    operands: OneToOne[OperandId, Operand],
    resolutions: OneToOne[OperandId, OperandResolution],
    instruction: Instruction,
    variants: List[MnemonicVariant],
) -> Tuple[
    Dict[MnemonicVariant, MnemonicBindings],
    Dict[MnemonicVariant, InstructionRejectionReason],
]:

    accepted: Dict[MnemonicVariant, MnemonicBindings] = {}
    rejected: Dict[MnemonicVariant, InstructionRejectionReason] = {}
    for variant in variants:
        reason: Optional[InstructionRejectionReason] = None

        # first check arity
        if len(instruction.operands) != len(variant):
            rejected[variant] = b"wrong-arity"
            continue

        # then check each operand
        for oid, spec in zip(instruction.operands, variant):

            # take provided operand
            operand: Operand = operands.get(oid)

            # if operand is a reference, try to resolve
            # but take only first acceptance, because
            # ambiguity will be reported elsewhere
            if operand.kind == b"reference":
                if resolution := resolutions.find(oid):
                    if resolved := resolution.accepted:
                        operand = Operand(
                            kind=resolved[0].kind,
                            target=resolved[0].target,
                        )

            # any reason requires immediate stop
            if reason := match_operand(operand, spec):
                break

        # finally, classify as accepted or rejected
        if reason is None:
            accepted[variant] = []
        else:
            rejected[variant] = reason

    return accepted, rejected


def build_resolution_by_instruction(
    operands: OneToOne[OperandId, Operand],
    instructions: OneToOne[InstructionId, Instruction],
    resolution_by_operand: OneToOne[OperandId, OperandResolution],
) -> OneToOne[InstructionId, InstructionResolution]:
    resolutions: Dict[InstructionId, InstructionResolution] = {}

    for iid, instruction in instructions.items():
        accepted: Dict[MnemonicVariant, MnemonicBindings] = {}
        rejected: Dict[MnemonicVariant, InstructionRejectionReason] = {}

        if variants := INSTRUCTIONS_TABLE.get(instruction.mnemonic.name):
            accepted, rejected = match_instruction(
                operands, resolution_by_operand, instruction, variants
            )

        acceptance = [
            InstructionAcceptance(
                mnemonic=instruction.mnemonic, variant=variant, bindings=bindings
            )
            for variant, bindings in accepted.items()
        ]

        rejection = [
            InstructionRejection(
                mnemonic=instruction.mnemonic, variant=variant, reason=reason
            )
            for variant, reason in rejected.items()
        ]

        resolutions[iid] = InstructionResolution(
            accepted=acceptance,
            rejected=rejection,
        )

    return OneToOne[InstructionId, InstructionResolution].instance(resolutions)
