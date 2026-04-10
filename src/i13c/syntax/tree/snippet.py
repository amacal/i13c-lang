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
    def on_bind(self, bind: Bind) -> None: ...

    # types related
    def on_type(self, type: types.Type) -> None: ...
    def on_range(self, range: types.Range) -> None: ...


@dataclass(kw_only=True, eq=False)
class Register:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor) -> None:
        visitor.on_operand(self)


@dataclass(kw_only=True, eq=False)
class Immediate:
    ref: Span
    value: literals.Hex

    def accept(self, visitor: Visitor) -> None:
        visitor.on_operand(self)


@dataclass(kw_only=True, eq=False)
class Reference:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor) -> None:
        visitor.on_operand(self)


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

    def accept(self, visitor: Visitor) -> None:
        visitor.on_operand(self)


Operand = Union[Register, Immediate, Reference, Address]


@dataclass(kw_only=True, eq=False)
class Bind:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor) -> None:
        visitor.on_bind(self)


@dataclass(kw_only=True, eq=False)
class Slot:
    name: bytes
    type: types.Type
    bind: Bind


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

        for entry in self.operands:
            entry.accept(visitor)


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

        for entry in self.slots:
            entry.bind.accept(visitor)
            entry.type.accept(visitor)

        for entry in self.instructions:
            entry.accept(visitor)
