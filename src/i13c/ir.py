from dataclasses import dataclass
from typing import List, Union


@dataclass
class MovRegImm:
    dst: int
    imm: int


@dataclass
class SysCall:
    pass


Instruction = Union[MovRegImm, SysCall]


@dataclass
class CodeBlock:
    label: bytes
    instructions: List[Instruction]
