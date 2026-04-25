from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Tuple

from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.resolutions.mnemonics import (
    MnemonicAcceptance,
    MnemonicVariant,
)
from i13c.semantic.typing.resolutions.operands import OperandAcceptance
from i13c.syntax.source import Span

InstructionRejectionReason = Kind[
    "arity-mismatch",
    "type-mismatch",
    "width-mismatch",
    "register-mismatch",
    "variant-mismatch",
]

OperandSymbol = Kind[
    "reg8", "reg16", "reg32", "reg64", "imm8", "imm16", "imm32", "imm64", "addr"
]


@dataclass(kw_only=True)
class InstructionRejection:
    ref: Span
    reason: InstructionRejectionReason


@dataclass(kw_only=True, frozen=True)
class OperandSpec:
    symbol: OperandSymbol
    names: Optional[Tuple[bytes, ...]]

    @staticmethod
    def reg8(*names: bytes) -> "OperandSpec":
        return OperandSpec(symbol="reg8", names=names)

    @staticmethod
    def reg16(*names: bytes) -> "OperandSpec":
        return OperandSpec(symbol="reg16", names=names)

    @staticmethod
    def reg32(*names: bytes) -> "OperandSpec":
        return OperandSpec(symbol="reg32", names=names)

    @staticmethod
    def reg64(*names: bytes) -> "OperandSpec":
        return OperandSpec(symbol="reg64", names=names)

    @staticmethod
    def imm8() -> "OperandSpec":
        return OperandSpec(symbol="imm8", names=())

    @staticmethod
    def imm16() -> "OperandSpec":
        return OperandSpec(symbol="imm16", names=())

    @staticmethod
    def imm32() -> "OperandSpec":
        return OperandSpec(symbol="imm32", names=())

    @staticmethod
    def imm64() -> "OperandSpec":
        return OperandSpec(symbol="imm64", names=())

    @staticmethod
    def addr() -> "OperandSpec":
        return OperandSpec(symbol="addr", names=())

    def __str__(self) -> str:
        if self.names is None:
            return self.symbol

        return ":".join(str(name) for name in (self.symbol, *self.names))


@dataclass(kw_only=True)
class InstructionAcceptance:
    ref: Span
    id: InstructionId

    mnemonic: MnemonicAcceptance
    variant: MnemonicVariant
    operands: Tuple[OperandAcceptance, ...]


@dataclass(kw_only=True)
class InstructionResolution:
    accepted: List[InstructionAcceptance]
    rejected: List[InstructionRejection]
