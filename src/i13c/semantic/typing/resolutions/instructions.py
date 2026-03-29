from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Tuple, Union

from i13c.semantic.core import Width
from i13c.semantic.typing.entities.instructions import Mnemonic
from i13c.semantic.typing.entities.operands import (
    REGISTERS_8,
    REGISTERS_64,
    Immediate,
    OperandKind,
    Reference,
    Register,
)

InstructionRejectionReason = Kind[
    b"arity-mismatch",
    b"type-mismatch",
    b"width-mismatch",
    b"register-mismatch",
    b"unresolved",
]


@dataclass(kw_only=True)
class InstructionRejection:
    mnemonic: Mnemonic
    variant: MnemonicVariant
    reason: InstructionRejectionReason


@dataclass(kw_only=True, frozen=True)
class OperandSpec:
    kind: OperandKind
    width: Tuple[Width, ...]
    names: Tuple[bytes, ...]

    @staticmethod
    def registers_8bit(*names: bytes) -> "OperandSpec":
        return OperandSpec(kind=b"register", width=(8,), names=names or REGISTERS_8)

    @staticmethod
    def registers_64bit(*names: bytes) -> "OperandSpec":
        return OperandSpec(kind=b"register", width=(64,), names=names or REGISTERS_64)

    @staticmethod
    def immediate(*width: Width) -> "OperandSpec":
        return OperandSpec(kind=b"immediate", width=width, names=())


MnemonicBindings = List[Union[Register, Immediate, Reference]]


@dataclass(kw_only=True)
class InstructionAcceptance:
    mnemonic: Mnemonic
    variant: MnemonicVariant
    bindings: MnemonicBindings


@dataclass(kw_only=True)
class InstructionResolution:
    accepted: List[InstructionAcceptance]
    rejected: List[InstructionRejection]


MnemonicVariant = Tuple[OperandSpec, ...]
