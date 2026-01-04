from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.sem.core import Width, derive_width


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
    kind: OperandKind
    target: OperandTarget

    @staticmethod
    def register(name: bytes) -> Operand:
        return Operand(kind=b"register", target=Register(name=name, width=64))

    @staticmethod
    def immediate(value: int) -> Operand:
        return Operand(
            kind=b"immediate", target=Immediate(value=value, width=derive_width(value))
        )

    @staticmethod
    def reference(name: bytes) -> Operand:
        return Operand(kind=b"reference", target=Reference(name=name))

    def describe(self) -> str:
        return self.kind[0:3].decode()
