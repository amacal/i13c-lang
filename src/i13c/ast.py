from typing import List, Union
from dataclasses import dataclass


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True)
class Immediate:
    value: int


@dataclass(kw_only=True)
class Instruction:
    mnemonic: bytes
    operands: List[Union[Register, Immediate]]


@dataclass(kw_only=True)
class Program:
    instructions: List[Instruction]
