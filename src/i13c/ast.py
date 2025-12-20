from typing import List, Union
from dataclasses import dataclass


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


@dataclass(kw_only=True)
class Program:
    instructions: List[Instruction]
