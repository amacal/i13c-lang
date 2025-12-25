from dataclasses import dataclass
from typing import List, Union

from i13c import src


@dataclass(kw_only=True, eq=False)
class Type:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Register:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Immediate:
    value: int


@dataclass(kw_only=True, eq=False)
class IntegerLiteral:
    ref: src.Span
    value: int


Literal = Union[IntegerLiteral]
Argument = Union[Literal]


@dataclass(kw_only=True, eq=False)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Instruction:
    ref: src.Span
    mnemonic: Mnemonic
    operands: List[Union[Register, Immediate]]


@dataclass(kw_only=True, eq=False)
class CallStatement:
    ref: src.Span
    name: bytes
    arguments: List[IntegerLiteral]


Statement = Union[CallStatement]


@dataclass(kw_only=True, eq=False)
class Slot:
    name: bytes
    type: Type
    bind: Register


@dataclass(kw_only=True, eq=False)
class Parameter:
    name: bytes
    type: Type


@dataclass(kw_only=True, eq=False)
class Snippet:
    ref: src.Span
    name: bytes
    terminal: bool
    slots: List[Slot]
    clobbers: List[Register]
    instructions: List[Instruction]


@dataclass(kw_only=True, eq=False)
class Function:
    ref: src.Span
    name: bytes
    terminal: bool
    parameters: List[Parameter]
    statements: List[CallStatement]


@dataclass(kw_only=True, eq=False)
class Program:
    functions: List[Function]
    snippets: List[Snippet]
