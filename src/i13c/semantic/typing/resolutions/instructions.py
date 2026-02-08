from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Tuple, Union

from i13c.semantic.core import Width
from i13c.semantic.typing.entities.instructions import Mnemonic
from i13c.semantic.typing.entities.operands import (
    Immediate,
    OperandKind,
    Reference,
    Register,
)

InstructionRejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
    b"width-mismatch",
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


MnemonicBindings = List[Union[Register, Immediate, Reference]]


@dataclass(kw_only=True)
class InstructionAcceptance:
    mnemonic: Mnemonic
    variant: MnemonicVariant
    bindings: MnemonicBindings

    def describe(self) -> str:
        variants = ":".join(var.describe() for var in self.variant)
        return f"mnemonic={self.mnemonic.name.decode():<8} variants={variants}"


@dataclass(kw_only=True)
class InstructionResolution:
    accepted: List[InstructionAcceptance]
    rejected: List[InstructionRejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )


MnemonicVariant = Tuple[OperandSpec, ...]
