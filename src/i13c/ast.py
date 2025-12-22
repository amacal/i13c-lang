from dataclasses import dataclass
from typing import List, Union


@dataclass(kw_only=True)
class Span:
    offset: int
    length: int


@dataclass
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True)
class Immediate:
    value: int


@dataclass(kw_only=True)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: List[Union[Register, Immediate]]


@dataclass
class Parameter:
    name: bytes
    type: Type
    bind: Register


@dataclass(kw_only=True)
class Function:
    ref: Span
    name: bytes
    terminal: bool
    clobbers: List[Register]
    parameters: List[Parameter]
    instructions: List[Instruction]


@dataclass(kw_only=True)
class Program:
    functions: List[Function]
