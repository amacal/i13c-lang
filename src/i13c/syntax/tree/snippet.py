from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Protocol, Union

import i13c.syntax.tree.literals as literals
import i13c.syntax.tree.types as types
from i13c.syntax.source import Span


class Visitor(Protocol):
    def on_snippet(self, snippet: Snippet) -> None: ...
    def on_instruction(self, instruction: Instruction) -> None: ...
    def on_operand(self, operand: Operand) -> None: ...


@dataclass(kw_only=True, eq=False)
class Register:
    ref: Span
    name: bytes


@dataclass(kw_only=True, eq=False)
class Immediate:
    ref: Span
    value: literals.Hex


@dataclass(kw_only=True, eq=False)
class Reference:
    ref: Span
    name: bytes


OffsetKind = Kind["forward", "backward"]


@dataclass(kw_only=True, eq=False)
class Offset:
    kind: OffsetKind
    value: literals.Hex


@dataclass(kw_only=True, eq=False)
class Address:
    ref: Span
    base: Register
    offset: Optional[Offset]


Operand = Union[Register, Immediate, Reference, Address]


@dataclass(kw_only=True)
class Binding:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Slot:
    name: bytes
    type: types.Type
    bind: Binding


@dataclass(kw_only=True, eq=False)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: List[Operand]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_instruction(self)

        for operand in self.operands:
            visitor.on_operand(operand)


@dataclass(kw_only=True, eq=False)
class Snippet:
    ref: Span
    name: bytes
    noreturn: bool
    slots: List[Slot]
    clobbers: List[Register]
    instructions: List[Instruction]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_snippet(self)

        for instruction in self.instructions:
            instruction.accept(visitor)
