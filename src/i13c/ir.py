from dataclasses import dataclass
from typing import List, Optional, Union


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
    label: Optional[bytes]
    noreturn: bool
    instructions: List[Instruction]


@dataclass
class Unit:
    entry: Optional[int]
    codeblocks: List[CodeBlock]
