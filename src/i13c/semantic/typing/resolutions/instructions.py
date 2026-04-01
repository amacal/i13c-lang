from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Tuple, Union

from i13c.semantic.core import Identifier, Width
from i13c.semantic.typing.entities.instructions import Mnemonic
from i13c.semantic.typing.entities.operands import (
    REGISTERS_8,
    REGISTERS_16,
    REGISTERS_32,
    REGISTERS_64,
    Address,
    Immediate,
    OperandId,
    OperandKind,
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
    def registers_16bit(*names: bytes) -> "OperandSpec":
        return OperandSpec(kind=b"register", width=(16,), names=names or REGISTERS_16)

    @staticmethod
    def registers_32bit(*names: bytes) -> "OperandSpec":
        return OperandSpec(kind=b"register", width=(32,), names=names or REGISTERS_32)

    @staticmethod
    def registers_64bit(*names: bytes) -> "OperandSpec":
        return OperandSpec(kind=b"register", width=(64,), names=names or REGISTERS_64)

    @staticmethod
    def immediate(*width: Width) -> "OperandSpec":
        return OperandSpec(kind=b"immediate", width=width, names=())

    @staticmethod
    def address_64bit() -> "OperandSpec":
        return OperandSpec(
            kind=b"address",
            width=(64,),
            names=(),
        )


@dataclass(kw_only=True)
class ReferenceToImmediate:
    target: OperandId
    identifier: Identifier


@dataclass(kw_only=True)
class ReferenceToRegister:
    target: OperandId
    identifier: Identifier


MnemonicBindingsItem = Union[Register, Immediate, Address, ReferenceToImmediate, ReferenceToRegister]
MnemonicBindings = List[MnemonicBindingsItem]


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
