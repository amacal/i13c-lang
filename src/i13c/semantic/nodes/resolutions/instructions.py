from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Optional, Tuple

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier, Type, Width
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.operands import (
    Address,
    Immediate,
    Operand,
    OperandId,
    Reference,
    Register,
)
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.resolutions.instructions import (
    InstructionAcceptance,
    InstructionRejection,
    InstructionRejectionReason,
    InstructionResolution,
    MnemonicBindings,
    MnemonicBindingsItem,
    MnemonicVariant,
    OperandSpec,
    ReferenceToImmediate,
    ReferenceToRegister,
)


def configure_resolution_by_instruction() -> GraphNode:
    return GraphNode(
        builder=build_resolution_by_instruction,
        constraint=None,
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
    b"add": [
        (OperandSpec.registers_64bit(), OperandSpec.immediate(8, 16, 32)),
        (OperandSpec.registers_64bit(), OperandSpec.registers_64bit()),
    ],
    b"bswap": [
        (OperandSpec.registers_32bit(),),
        (OperandSpec.registers_64bit(),),
    ],
    b"lea": [
        (OperandSpec.registers_32bit(), OperandSpec.address_64bit()),
        (OperandSpec.registers_64bit(), OperandSpec.address_64bit()),
    ],
    b"mov": [
        (OperandSpec.registers_64bit(), OperandSpec.immediate(8, 16, 32, 64)),
        (OperandSpec.registers_64bit(), OperandSpec.registers_64bit()),
        (OperandSpec.address_64bit(), OperandSpec.immediate(8, 16, 32)),
        (OperandSpec.address_64bit(), OperandSpec.registers_64bit()),
        (OperandSpec.registers_64bit(), OperandSpec.address_64bit()),
    ],
    b"shl": [
        (OperandSpec.registers_8bit(), OperandSpec.immediate(8)),
        (OperandSpec.registers_16bit(), OperandSpec.immediate(8)),
        (OperandSpec.registers_32bit(), OperandSpec.immediate(8)),
        (OperandSpec.registers_64bit(), OperandSpec.immediate(8)),
        (OperandSpec.registers_64bit(), OperandSpec.registers_8bit(b"cl")),
    ],
    b"syscall": [()],
}

OperandSubstituteKind = Kind[b"register", b"immediate", b"address"]


@dataclass(kw_only=True)
class OperandSubstitute:
    kind: OperandSubstituteKind
    width: Width
    registers: Optional[Tuple[bytes, ...]]


def match_operand(
    operand: OperandSubstitute, spec: OperandSpec
) -> Optional[InstructionRejectionReason]:

    if operand.kind != spec.kind:
        return b"type-mismatch"

    # on purpose we match exactly the width even for immediates
    # because instruction variants are defined that way; we can
    # have full control over which immediate widths are allowed

    if operand.width not in spec.width:
        return b"width-mismatch"

    # if the spec and operand are registers aware, we need
    # to check if we all operand registers are allowed by the spec

    if operand.registers is not None and operand.registers:
        if len(set(spec.names).intersection(operand.registers)) != len(
            operand.registers
        ):
            return b"register-mismatch"

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
            rejected[variant] = b"arity-mismatch"
            continue

        # then check each operand
        for oid, spec in zip(instruction.operands, variant):

            # take provided operand
            operand = operands.get(oid)
            target: Optional[MnemonicBindingsItem] = None
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
                        registers=None,
                    )

                    # remember immediate as a target
                    identifier = Identifier(name=operand.target.name)
                    target = ReferenceToImmediate(target=oid, identifier=identifier)

                # else try to resolve as register
                if operand.target.name in registers:
                    substitute = OperandSubstitute(
                        kind=b"register",
                        width=registers[operand.target.name].width,
                        registers=(registers[operand.target.name].name,),
                    )

                    # remember register as a target
                    identifier = Identifier(name=operand.target.name)
                    target = ReferenceToRegister(target=oid, identifier=identifier)

                # if we could not resolve, mark as such
                if substitute is None:
                    reason = b"unresolved"
                    break

            # try to extract immediate directly
            elif operand.kind == b"immediate":

                # satisfy type constraints
                assert isinstance(operand.target, Immediate)

                # remember immediate as a target
                target = operand.target

                substitute = OperandSubstitute(
                    kind=operand.kind,
                    width=operand.target.width,
                    registers=None,
                )

            # try to extract register directly
            elif operand.kind == b"register":

                # satisfy type constraints
                assert isinstance(operand.target, Register)

                # remember register as a target
                target = operand.target

                substitute = OperandSubstitute(
                    kind=operand.kind,
                    width=operand.target.width,
                    registers=(operand.target.name,),
                )

            # otherwise, try to extract address directly
            else:

                # satisfy type constraints
                assert isinstance(operand.target, Address)

                # remember address as a target
                target = operand.target

                substitute = OperandSubstitute(
                    kind=operand.kind,
                    width=64,
                    registers=None,
                )

            # any reason requires immediate stop
            if reason := match_operand(substitute, spec):
                break

            assert target is not None
            bindings.append(target)

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
