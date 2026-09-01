from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.mnemonics import Mnemonic, MnemonicId
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
    "addr8",
    "addr16",
    "addr32",
    "addr64",
    "rel",
]


@dataclass(kw_only=True)
class MnemonicRejection:
    ref: Span
    id: MnemonicId

    target: Mnemonic
    reason: MnemonicRejectionReason


@dataclass(kw_only=True, frozen=True)
class MnemonicOperandSpec:
    symbol: MnemonicOperandSymbol
    names: tuple[bytes, ...] | None

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
    def addr8() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="addr8", names=())

    @staticmethod
    def addr16() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="addr16", names=())

    @staticmethod
    def addr32() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="addr32", names=())

    @staticmethod
    def addr64() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="addr64", names=())

    @staticmethod
    def rel() -> MnemonicOperandSpec:
        return MnemonicOperandSpec(symbol="rel", names=())

    def __repr__(self) -> str:
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
    variants: list[MnemonicVariant]


@dataclass(kw_only=True)
class MnemonicResolution:
    ref: Span
    id: MnemonicId

    accepted: list[MnemonicAcceptance]
    rejected: list[MnemonicRejection]


MnemonicVariant = tuple[MnemonicOperandSpec, ...]
