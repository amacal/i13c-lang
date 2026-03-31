from dataclasses import dataclass
from typing import Literal as Kind
from typing import Optional, Tuple, Union

from i13c.semantic.core import Width, derive_width
from i13c.syntax.source import Span

# fmt: off
REGISTERS_8: Tuple[bytes, ...] = (
    b"al", b"bl", b"cl", b"dl", b"sil", b"dil", b"bpl", b"spl",
    b"r8b", b"r9b", b"r10b", b"r11b", b"r12b", b"r13b", b"r14b", b"r15b",
)

REGISTERS_64: Tuple[bytes, ...] = (
    b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp",
    b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15",
)
# fmt: on


@dataclass(kw_only=True)
class Register:
    name: bytes
    width: Width

    @staticmethod
    def from_name(name: bytes) -> Register:
        if name in REGISTERS_8:
            return Register(name=name, width=8)

        if name in REGISTERS_64:
            return Register(name=name, width=64)

        raise ValueError(f"unknown register: {name!r}")

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Immediate:
    value: int
    width: Width

    @staticmethod
    def from_value(value: int) -> Immediate:
        return Immediate(value=value, width=derive_width(abs(value)))

    @staticmethod
    def optional(value: Optional[int]) -> Optional[Immediate]:
        return Immediate.from_value(value) if value is not None else None


@dataclass(kw_only=True)
class Reference:
    name: bytes


@dataclass(kw_only=True)
class Address:
    base: Register
    offset: Optional[Immediate]


OperandKind = Kind[b"register", b"immediate", b"reference", b"address"]
OperandTarget = Union[Register, Immediate, Reference, Address]


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
            target=Register.from_name(name),
        )

    @staticmethod
    def immediate(ref: Span, value: int) -> Operand:
        return Operand(
            ref=ref,
            kind=b"immediate",
            target=Immediate.from_value(value),
        )

    @staticmethod
    def reference(ref: Span, name: bytes) -> Operand:
        return Operand(
            ref=ref,
            kind=b"reference",
            target=Reference(name=name),
        )

    @staticmethod
    def address(ref: Span, base: Register, offset: Optional[Immediate]) -> Operand:
        return Operand(
            ref=ref,
            kind=b"address",
            target=Address(base=base, offset=offset),
        )
