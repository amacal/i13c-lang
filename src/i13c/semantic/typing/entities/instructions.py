from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.operands import OperandId
from i13c.src import Span

BindingKind = Kind[b"register", b"immediate"]


@dataclass(kw_only=True)
class Binding:
    kind: BindingKind
    name: bytes

    @staticmethod
    def register(name: bytes) -> Binding:
        return Binding(kind=b"register", name=name)

    @staticmethod
    def immediate() -> Binding:
        return Binding(kind=b"immediate", name=b"imm")

    def via_immediate(self) -> bool:
        return self.kind == b"immediate"

    def via_register(self) -> bool:
        return self.kind == b"register"

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Mnemonic:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: List[OperandId]

    def describe(self) -> str:
        operands = ":".join(op.identify(2) for op in self.operands)
        return f"mnemonic={self.mnemonic.name.decode():<8} operands={operands}"
