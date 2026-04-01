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

REGISTERS_16: Tuple[bytes, ...] = (
    b"ax", b"bx", b"cx", b"dx", b"si", b"di", b"sp", b"bp",
    b"r8w", b"r9w", b"r10w", b"r11w", b"r12w", b"r13w", b"r14w", b"r15w",
)

REGISTERS_32: Tuple[bytes, ...] = (
    b"eax", b"ebx", b"ecx", b"edx", b"esi", b"edi", b"esp", b"ebp",
    b"r8d", b"r9d", b"r10d", b"r11d", b"r12d", b"r13d", b"r14d", b"r15d",
)

REGISTERS_64: Tuple[bytes, ...] = (
    b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp",
    b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15",
)
# fmt: on

OperandSymbol = Kind[
    b"reg8",
    b"reg16",
    b"reg32",
    b"reg64",
    b"imm8",
    b"imm16",
    b"imm32",
    b"imm64",
    b"addr",
]


@dataclass(kw_only=True)
class Register:
    name: bytes
    width: Width

    @staticmethod
    def from_name(name: bytes) -> Register:
        if name in REGISTERS_8:
            return Register(name=name, width=8)

        if name in REGISTERS_16:
            return Register(name=name, width=16)

        if name in REGISTERS_32:
            return Register(name=name, width=32)

        if name in REGISTERS_64:
            return Register(name=name, width=64)

        raise ValueError(f"unknown register: {name!r}")

    def symbol(self) -> OperandSymbol:
        if self.width == 8:
            return b"reg8"

        if self.width == 16:
            return b"reg16"

        if self.width == 32:
            return b"reg32"

        return b"reg64"

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

    def symbol(self) -> OperandSymbol:
        if self.width == 8:
            return b"imm8"

        if self.width == 16:
            return b"imm16"

        if self.width == 32:
            return b"imm32"

        return b"imm64"


@dataclass(kw_only=True)
class Reference:
    name: bytes

    def symbol(self) -> OperandSymbol:
        assert False


@dataclass(kw_only=True)
class Address:
    base: Register
    offset: Optional[Immediate]

    def symbol(self) -> OperandSymbol:
        return b"addr"


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
