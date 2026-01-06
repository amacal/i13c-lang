from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from i13c.core.mapping import OneToOne
from i13c.sem.core import Type, Width
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.instructions import Instruction, InstructionId
from i13c.sem.typing.entities.operands import (
    Immediate,
    Operand,
    OperandId,
    OperandKind,
    Reference,
    Register,
)
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.resolutions.instructions import (
    InstructionAcceptance,
    InstructionRejection,
    InstructionRejectionReason,
    InstructionResolution,
    MnemonicBindings,
    MnemonicVariant,
    OperandSpec,
)


def configure_resolution_by_instruction() -> Configuration:
    return Configuration(
        builder=build_resolution_by_instruction,
        produces=("resolutions/instructions",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("operands", "entities/operands"),
                ("snippets", "entities/snippets"),
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


@dataclass(kw_only=True)
class OperandSubstitute:
    kind: OperandKind
    width: Width


def match_operand(
    operand: OperandSubstitute, spec: OperandSpec
) -> Optional[InstructionRejectionReason]:

    if operand.kind != spec.kind:
        return b"type-mismatch"

    # on purpose we match exactly the width even for immediates
    # because instruction variants are defined that way; we can
    # have full control over which immediate widths are allowed

    if operand.width != spec.width:
        return b"width-mismatch"

    return None


def match_instruction(
    operands: OneToOne[OperandId, Operand],
    immediates: Dict[bytes, Type],
    registers: Dict[bytes, Register],
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
        bindings: MnemonicBindings = []

        # first check arity
        if len(instruction.operands) != len(variant):
            rejected[variant] = b"wrong-arity"
            continue

        # then check each operand
        for oid, spec in zip(instruction.operands, variant):

            # take provided operand
            operand = operands.get(oid)
            substitute: Optional[OperandSubstitute] = None

            # if operand is a reference, try to resolve
            # from provided immediate type mapping
            if operand.kind == b"reference":

                # satisfy type constraints
                assert isinstance(operand.target, Reference)

                # try to resolve from immediates mapping
                if operand.target.name in immediates:
                    substitute = OperandSubstitute(
                        kind=b"immediate",
                        width=immediates[operand.target.name].width,
                    )

                # else try to resolve as register
                if operand.target.name in registers:
                    substitute = OperandSubstitute(
                        kind=b"register",
                        width=registers[operand.target.name].width,
                    )

                # if we could not resolve, mark as such
                if substitute is None:
                    reason = b"unresolved"
                    break

            # try to extract immediate directly
            elif operand.kind == b"immediate":
                # satisfy type constraints
                assert isinstance(operand.target, Immediate)

                substitute = OperandSubstitute(
                    kind=operand.kind,
                    width=operand.target.width,
                )

            # otherwise it has to be a register
            else:
                # satisfy type constraints
                assert isinstance(operand.target, Register)

                substitute = OperandSubstitute(
                    kind=operand.kind,
                    width=operand.target.width,
                )

            # any reason requires immediate stop
            if reason := match_operand(substitute, spec):
                break

            bindings.append(operand.target)

        # finally, classify as accepted with bindings
        # or rejected with determined reason
        if reason is None:
            accepted[variant] = bindings
        else:
            rejected[variant] = reason

    return accepted, rejected


def build_resolution_by_instruction(
    operands: OneToOne[OperandId, Operand],
    snippets: OneToOne[SnippetId, Snippet],
    instructions: OneToOne[InstructionId, Instruction],
) -> OneToOne[InstructionId, InstructionResolution]:
    resolutions: Dict[InstructionId, InstructionResolution] = {}

    for snippet in snippets.values():
        immediates: Dict[bytes, Type] = {}
        registers: Dict[bytes, Register] = {}

        # collect immediate slots
        for slot in snippet.slots:
            if slot.bind.via_immediate():
                immediates[slot.name.name] = slot.type
            else:
                registers[slot.name.name] = Register(
                    name=slot.bind.name,
                    width=64,
                )

        # don't attempt to match instructions if names are not unique
        if len(immediates.keys() | registers.keys()) < len(snippet.slots):
            continue

        for iid in snippet.instructions:
            accepted: Dict[MnemonicVariant, MnemonicBindings] = {}
            rejected: Dict[MnemonicVariant, InstructionRejectionReason] = {}

            # retrieve instruction
            instruction = instructions.get(iid)

            # if instruction mnemonic is known, try to match
            if variants := INSTRUCTIONS_TABLE.get(instruction.mnemonic.name):
                args = (operands, immediates, registers, instruction, variants)
                accepted, rejected = match_instruction(*args)

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
