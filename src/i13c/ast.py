from dataclasses import dataclass
from typing import List, Union

from i13c import src


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True)
class Immediate:
    value: int


@dataclass(kw_only=True)
class IntegerLiteral:
    value: int


@dataclass(kw_only=True)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True)
class Instruction:
    ref: src.Span
    mnemonic: Mnemonic
    operands: List[Union[Register, Immediate]]


@dataclass(kw_only=True)
class CallStatement:
    ref: src.Span
    name: bytes
    arguments: List[IntegerLiteral]


@dataclass(kw_only=True)
class AsmParameter:
    name: bytes
    type: Type
    bind: Register


@dataclass(kw_only=True)
class RegParameter:
    name: bytes
    type: Type


@dataclass(kw_only=True)
class AsmFunction:
    ref: src.Span
    name: bytes
    terminal: bool
    clobbers: List[Register]
    parameters: List[AsmParameter]
    instructions: List[Instruction]


@dataclass(kw_only=True)
class RegFunction:
    ref: src.Span
    name: bytes
    terminal: bool
    parameters: List[RegParameter]
    statements: List[CallStatement]


@dataclass(kw_only=True)
class Program:
    functions: List[Union[AsmFunction, RegFunction]]
