from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Tuple, Union

from i13c.sem.core import Width, derive_width
from i13c.src import Span

# AllowedVariants = Union[Type[Register], Type[Immediate]]


# @dataclass(kw_only=True)
# class InstructionSignature:
#     variants: List[Tuple[AllowedVariants, ...]]


# INSTRUCTIONS_TABLE = {
#     b"syscall": InstructionSignature(variants=[()]),
#     b"mov": InstructionSignature(variants=[(Register, Immediate)]),
# }

OperandKind = Kind[b"register", b"immediate"]


@dataclass(kw_only=True)
class Register:
    name: bytes


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


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int


@dataclass(kw_only=True)
class Instruction:
    id: InstructionId
    ref: Span
    mnemonic: Mnemonic
    operands: List[Operand]


@dataclass(kw_only=True)
class OperandSpec:
    kind: OperandKind
    width: Width


@dataclass(kw_only=True)
class InstructionSpec:
    mnemonic: Mnemonic
    operands: Tuple[OperandSpec, ...]


@dataclass(kw_only=True)
class InstructionAcceptance:
    spec: InstructionSpec


InstructionRejectionReason = Kind[
    b"unknown-mnemonic",
    b"wrong-arity",
    b"type-mismatch",
    b"width-mismatch",
]


@dataclass(kw_only=True)
class InstructionRejection:
    spec: InstructionSpec
    reason: InstructionRejectionReason


@dataclass(kw_only=True)
class InstructionResolution:
    accepted: List[InstructionAcceptance]
    rejected: List[InstructionRejection]
