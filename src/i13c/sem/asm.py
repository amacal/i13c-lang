from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Optional, Tuple, Union

from i13c import ast
from i13c.sem.core import Width, derive_width
from i13c.sem.syntax import SyntaxGraph
from i13c.src import Span

OperandKind = Kind[b"register", b"immediate"]


@dataclass(kw_only=True)
class Register:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Immediate:
    value: int
    width: Optional[Width]


@dataclass(kw_only=True)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True)
class Operand:
    kind: OperandKind
    target: Union[Register, Immediate]

    @staticmethod
    def register(name: bytes) -> "Operand":
        return Operand(kind=b"register", target=Register(name=name))

    @staticmethod
    def immediate(value: int) -> "Operand":
        return Operand(
            kind=b"immediate", target=Immediate(value=value, width=derive_width(value))
        )

    def describe(self) -> str:
        return self.kind[0:3].decode()


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: List[Operand]

    def describe(self) -> str:
        operands = ":".join(op.describe() for op in self.operands)
        return f"mnemonic={self.mnemonic.name.decode():<8} operands={operands}"


@dataclass(kw_only=True, frozen=True)
class OperandSpec:
    kind: OperandKind
    width: Optional[Width]

    def __str__(self) -> str:
        return f"{self.kind.decode()}:({self.width})"

    @staticmethod
    def register() -> "OperandSpec":
        return OperandSpec(kind=b"register", width=64)

    @staticmethod
    def immediate(width: Width) -> "OperandSpec":
        return OperandSpec(kind=b"immediate", width=width)

    def describe(self) -> str:
        return self.kind[0:3].decode()


@dataclass(kw_only=True)
class Acceptance:
    mnemonic: Mnemonic
    variant: MnemonicVariant

    def describe(self) -> str:
        variants = ":".join(var.describe() for var in self.variant)
        return f"mnemonic={self.mnemonic.name.decode():<8} variants={variants}"


RejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
    b"width-mismatch",
]


@dataclass(kw_only=True)
class Rejection:
    mnemonic: Mnemonic
    variant: MnemonicVariant
    reason: RejectionReason


@dataclass(kw_only=True)
class Resolution:
    accepted: List[Acceptance]
    rejected: List[Rejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )


MnemonicVariant = Tuple[OperandSpec, ...]

INSTRUCTIONS_TABLE: Dict[bytes, List[MnemonicVariant]] = {
    b"syscall": [()],
    b"mov": [
        (OperandSpec.register(), OperandSpec.immediate(64)),
        (OperandSpec.register(), OperandSpec.immediate(32)),
        (OperandSpec.register(), OperandSpec.immediate(16)),
        (OperandSpec.register(), OperandSpec.immediate(8)),
    ],
}


def match_operand(operand: Operand, spec: OperandSpec) -> Optional[RejectionReason]:
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
    instruction: Instruction, variants: List[MnemonicVariant]
) -> Tuple[List[MnemonicVariant], Dict[MnemonicVariant, RejectionReason]]:

    accepted: List[MnemonicVariant] = []
    rejected: Dict[MnemonicVariant, RejectionReason] = {}

    for variant in variants:
        reason: Optional[RejectionReason] = None

        # first check arity
        if len(instruction.operands) != len(variant):
            rejected[variant] = b"wrong-arity"
            continue

        # then check each operand
        for operand, spec in zip(instruction.operands, variant):
            if reason := match_operand(operand, spec):
                break

        # finally, classify as accepted or rejected
        if reason is None:
            accepted.append(variant)
        else:
            rejected[variant] = reason

    return accepted, rejected


def build_instructions(
    graph: SyntaxGraph,
) -> Dict[InstructionId, Instruction]:
    instructions: Dict[InstructionId, Instruction] = {}

    for nid, instruction in graph.instructions.items():
        operands: List[Operand] = []

        for operand in instruction.operands:
            match operand:
                case ast.Register() as reg:
                    operands.append(Operand.register(name=reg.name))
                case ast.Immediate() as imm:
                    operands.append(Operand.immediate(value=imm.value))

        # derive instruction ID from globally unique node ID
        instruction_id = InstructionId(value=nid.value)

        instructions[instruction_id] = Instruction(
            ref=instruction.ref,
            mnemonic=Mnemonic(name=instruction.mnemonic.name),
            operands=operands,
        )

    return instructions


def build_resolutions(
    instructions: Dict[InstructionId, Instruction],
) -> Dict[InstructionId, Resolution]:
    resolutions: Dict[InstructionId, Resolution] = {}

    for iid, instruction in instructions.items():
        accepted: List[MnemonicVariant] = []
        rejected: Dict[MnemonicVariant, RejectionReason] = {}

        if variants := INSTRUCTIONS_TABLE.get(instruction.mnemonic.name):
            accepted, rejected = match_instruction(instruction, variants)

        acceptance = [
            Acceptance(mnemonic=instruction.mnemonic, variant=variant)
            for variant in accepted
        ]

        rejection = [
            Rejection(mnemonic=instruction.mnemonic, variant=variant, reason=reason)
            for variant, reason in rejected.items()
        ]

        resolutions[iid] = Resolution(
            accepted=acceptance,
            rejected=rejection,
        )

    return resolutions
