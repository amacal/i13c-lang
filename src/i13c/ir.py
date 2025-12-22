from dataclasses import dataclass
from typing import List, Set, Union


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


@dataclass
class Unit:
    symbols: Set[bytes]
    codeblocks: List[CodeBlock]
