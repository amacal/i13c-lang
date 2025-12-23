from dataclasses import dataclass
from typing import List, Union

from i13c import src


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
    ref: src.Span
    mnemonic: Mnemonic
    operands: List[Union[Register, Immediate]]


@dataclass
class Parameter:
    name: bytes
    type: Type
    bind: Register


@dataclass(kw_only=True)
class Function:
    ref: src.Span
    name: bytes
    terminal: bool
    clobbers: List[Register]
    parameters: List[Parameter]
    instructions: List[Instruction]


@dataclass(kw_only=True)
class Program:
    functions: List[Function]
