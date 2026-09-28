from dataclasses import dataclass
from typing import Literal as Kind
from typing import Protocol

from i13c.syntax.source import Span
from i13c.syntax.tree import literals, types
from i13c.syntax.tree.core import Path


class Visitor(Protocol):
    def on_snippet(self, snippet: Snippet, path: Path): ...
    def on_flags(self, flags: Flags, path: Path): ...
    def on_signature(self, signature: Signature, path: Path): ...
    def on_slot(self, slot: Slot, path: Path): ...
    def on_bind(self, bind: Bind, path: Path): ...
    def on_result(self, result: Result, path: Path): ...
    def on_label(self, label: Label, path: Path): ...
    def on_instruction(self, instruction: Instruction, path: Path): ...
    def on_mnemonic(self, mnemonic: Mnemonic, path: Path): ...
    def on_operand(self, operand: Operand, path: Path): ...
    def on_immediate(self, immediate: Immediate, path: Path): ...
    def on_register(self, register: Register, path: Path): ...
    def on_reference(self, reference: Reference, path: Path): ...
    def on_address(self, address: Address, path: Path): ...
    def on_index(self, index: Index, path: Path): ...
    def on_displacement(self, displacement: Displacement, path: Path): ...

    # types related
    def on_type(self, type: types.Type, path: Path): ...
    def on_range(self, range: types.Range, path: Path): ...


@dataclass(kw_only=True, eq=False)
class Register:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_register(self, path)


@dataclass(kw_only=True, eq=False)
class Immediate:
    ref: Span
    data: literals.Hex

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_immediate(self, path)


@dataclass(kw_only=True, eq=False)
class Reference:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_reference(self, path)


@dataclass(kw_only=True, eq=False)
class Index:
    ref: Span

    scale: int
    target: Register | Reference

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_index(self, path)

        with path.push(self) as node:
            self.target.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Displacement:
    ref: Span
    kind: Kind["forward", "backward"]
    offset: literals.Hex

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_displacement(self, path)


@dataclass(kw_only=True, eq=False)
class Address:
    ref: Span
    size: bytes | None
    base: Register | Reference | None
    indx: Index | None
    disp: Displacement | Reference | None

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_address(self, path)

        with path.push(self) as node:
            if self.base is not None:
                self.base.accept(visitor, node)

            if self.indx is not None:
                self.indx.accept(visitor, node)

            if self.disp is not None:
                self.disp.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Label:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_label(self, path)


OperandTarget = Register | Immediate | Reference | Address


@dataclass(kw_only=True, eq=False)
class Operand:
    ref: Span
    target: OperandTarget

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_operand(self, path)

        with path.push(self) as node:
            self.target.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Bind:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_bind(self, path)


@dataclass(kw_only=True, eq=False)
class Result:
    ref: Span
    type: types.Type
    bind: Bind

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_result(self, path)

        with path.push(self) as node:
            self.bind.accept(visitor, node)
            self.type.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Slot:
    ref: Span
    name: bytes
    type: types.Type
    bind: Bind

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_slot(self, path)

        with path.push(self) as node:
            self.bind.accept(visitor, node)
            self.type.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Mnemonic:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_mnemonic(self, path)


@dataclass(kw_only=True, eq=False)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: list[Operand]

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_instruction(self, path)

        with path.push(self) as node:
            self.mnemonic.accept(visitor, node)

            for entry in self.operands:
                entry.accept(visitor, node)


InstructionOrLabel = Instruction | Label


@dataclass(kw_only=True, eq=False)
class Signature:
    ref: Span
    name: bytes
    slots: list[Slot]
    result: Result | None

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_signature(self, path)

        with path.push(self) as node:
            for entry in self.slots:
                entry.accept(visitor, node)

            if self.result is not None:
                self.result.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Flags:
    ref: Span
    noreturn: bool | None
    clobbers: list[Register] | None

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_flags(self, path)

        with path.push(self) as node:
            for entry in self.clobbers or []:
                entry.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Snippet:
    ref: Span
    signature: Signature
    flags: Flags | None
    body: list[InstructionOrLabel]

    def accept(self, visitor: Visitor, path: Path):
        visitor.on_snippet(self, path)

        with path.push(self) as node:
            self.signature.accept(visitor, node)

            if self.flags is not None:
                self.flags.accept(visitor, node)

            for entry in self.body:
                entry.accept(visitor, node)
