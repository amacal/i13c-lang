from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.sem.core import Width, derive_width
from i13c.src import Span


@dataclass(kw_only=True)
class Register:
    name: bytes
    width: Width

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Immediate:
    value: int
    width: Width


@dataclass(kw_only=True)
class Reference:
    name: bytes


OperandKind = Kind[b"register", b"immediate", b"reference"]
OperandTarget = Union[Register, Immediate, Reference]


@dataclass(kw_only=True, frozen=True)
class OperandId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("operand", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Operand:
    ref: Span
    kind: OperandKind
    target: OperandTarget

    @staticmethod
    def register(ref: Span, name: bytes) -> Operand:
        return Operand(
            ref=ref,
            kind=b"register",
            target=Register(name=name, width=64),
        )

    @staticmethod
    def immediate(ref: Span, value: int) -> Operand:
        return Operand(
            ref=ref,
            kind=b"immediate",
            target=Immediate(value=value, width=derive_width(value)),
        )

    @staticmethod
    def reference(ref: Span, name: bytes) -> Operand:
        return Operand(
            ref=ref,
            kind=b"reference",
            target=Reference(name=name),
        )

    def describe(self) -> str:
        return self.kind[0:3].decode()
