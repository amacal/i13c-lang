from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Tuple

from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.syntax.source import Span

MnemonicRejectionReason = Kind["unknown-mnemonic",]

MnemonicOperandSymbol = Kind[
    "reg8",
    "reg16",
    "reg32",
    "reg64",
    "imm8",
    "imm16",
    "imm32",
    "imm64",
    "addr",
    "rel",
]


@dataclass(kw_only=True)
class MnemonicRejection:
    ref: Span
    reason: MnemonicRejectionReason


@dataclass(kw_only=True, frozen=True)
class MnemonicOperandSpec:
    symbol: MnemonicOperandSymbol
    names: Optional[Tuple[bytes, ...]]

    @staticmethod
    def reg8(*names: bytes) -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="reg8", names=names)

    @staticmethod
    def reg16(*names: bytes) -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="reg16", names=names)

    @staticmethod
    def reg32(*names: bytes) -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="reg32", names=names)

    @staticmethod
    def reg64(*names: bytes) -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="reg64", names=names)

    @staticmethod
    def imm8() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="imm8", names=())

    @staticmethod
    def imm16() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="imm16", names=())

    @staticmethod
    def imm32() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="imm32", names=())

    @staticmethod
    def imm64() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="imm64", names=())

    @staticmethod
    def addr() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="addr", names=())

    @staticmethod
    def rel() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="rel", names=())

    def __str__(self) -> str:
        if self.names is None:
            return self.symbol

        return ":".join(
            str(name) for name in (self.symbol, *[name.decode() for name in self.names])
        )


@dataclass(kw_only=True)
class MnemonicAcceptance:
    ref: Span
    id: MnemonicId

    name: bytes
    variants: List[MnemonicVariant]


@dataclass(kw_only=True)
class MnemonicResolution:
    accepted: List[MnemonicAcceptance]
    rejected: List[MnemonicRejection]


MnemonicVariant = Tuple[MnemonicOperandSpec, ...]
