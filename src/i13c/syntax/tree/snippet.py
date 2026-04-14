from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Protocol, Union

import i13c.syntax.tree.literals as literals
import i13c.syntax.tree.types as types
from i13c.syntax.source import Span
from i13c.syntax.tree.core import Path


class Visitor(Protocol):
    def on_snippet(self, snippet: Snippet, path: Path) -> None: ...
    def on_signature(self, signature: Signature, path: Path) -> None: ...
    def on_slot(self, slot: Slot, path: Path) -> None: ...
    def on_bind(self, bind: Bind, path: Path) -> None: ...
    def on_label(self, label: Label, path: Path) -> None: ...
    def on_instruction(self, instruction: Instruction, path: Path) -> None: ...
    def on_operand(self, operand: Operand, path: Path) -> None: ...
    def on_immediate(self, immediate: Immediate, path: Path) -> None: ...
    def on_register(self, register: Register, path: Path) -> None: ...
    def on_reference(self, reference: Reference, path: Path) -> None: ...
    def on_address(self, address: Address, path: Path) -> None: ...

    # types related
    def on_type(self, type: types.Type, path: Path) -> None: ...
    def on_range(self, range: types.Range, path: Path) -> None: ...


@dataclass(kw_only=True, eq=False)
class Register:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_operand(self, path)
        visitor.on_register(self, path)


@dataclass(kw_only=True, eq=False)
class Immediate:
    ref: Span
    value: literals.Hex

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_operand(self, path)
        visitor.on_immediate(self, path)


@dataclass(kw_only=True, eq=False)
class Reference:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_operand(self, path)
        visitor.on_reference(self, path)


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

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_operand(self, path)
        visitor.on_address(self, path)


Operand = Union[Register, Immediate, Reference, Address]


@dataclass(kw_only=True, eq=False)
class Bind:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_bind(self, path)


@dataclass(kw_only=True, eq=False)
class Slot:
    ref: Span
    name: bytes
    type: types.Type
    bind: Bind

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_slot(self, path)

        with path.push(self) as node:
            self.bind.accept(visitor, node)
            self.type.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: List[Operand]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_instruction(self, path)

        with path.push(self) as node:
            for entry in self.operands:
                entry.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Label:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_label(self, path)


InstructionOrLabel = Union[Instruction, Label]


@dataclass(kw_only=True, eq=False)
class Signature:
    ref: Span
    name: bytes
    slots: List[Slot]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_signature(self, path)

        with path.push(self) as node:
            for entry in self.slots:
                entry.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Snippet:
    ref: Span
    noreturn: bool
    signature: Signature
    clobbers: List[Register]
    body: List[InstructionOrLabel]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_snippet(self, path)

        with path.push(self) as node:
            self.signature.accept(visitor, node)

            for entry in self.body:
                entry.accept(visitor, node)
