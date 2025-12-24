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
class AsmParameter:
    name: bytes
    type: Type
    bind: Register


@dataclass(kw_only=True, eq=False)
class RegParameter:
    name: bytes
    type: Type


Parameter = Union[AsmParameter, RegParameter]


@dataclass(kw_only=True, eq=False)
class AsmFunction:
    ref: src.Span
    name: bytes
    terminal: bool
    clobbers: List[Register]
    parameters: List[AsmParameter]
    instructions: List[Instruction]


@dataclass(kw_only=True, eq=False)
class RegFunction:
    ref: src.Span
    name: bytes
    terminal: bool
    parameters: List[RegParameter]
    statements: List[CallStatement]


Function = Union[AsmFunction, RegFunction]


@dataclass(kw_only=True, eq=False)
class Program:
    functions: List[Function]
