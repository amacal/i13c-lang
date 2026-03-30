from dataclasses import dataclass
from typing import Literal as Kind
from typing import Tuple, Union

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
        width = 64

        if name in REGISTERS_8:
            width = 8

        return Operand(
            ref=ref,
            kind=b"register",
            target=Register(name=name, width=width),
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

    # @staticmethod
    # def address(ref: Span, base: OperandTarget, offset: Union[Immediate, Register, Reference]) -> Operand:
    #     pass
