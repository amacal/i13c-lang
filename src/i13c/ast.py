from dataclasses import dataclass
from typing import List, Union


@dataclass(kw_only=True)
class Reference:
    offset: int
    length: int


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
    ref: Reference
    mnemonic: Mnemonic
    operands: List[Union[Register, Immediate]]


@dataclass
class Parameter:
    name: bytes
    type: bytes
    bind: bytes


@dataclass(kw_only=True)
class Function:
    name: bytes
    clobbers: List[bytes]
    parameters: List[Parameter]
    instructions: List[Instruction]


@dataclass(kw_only=True)
class Program:
    functions: List[Function]
