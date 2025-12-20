from typing import Union
from dataclasses import dataclass


@dataclass
class MovRegImm:
    dst: int
    imm: int


@dataclass
class SysCall:
    pass


Instruction = Union[MovRegImm, SysCall]
