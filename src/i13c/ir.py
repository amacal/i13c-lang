from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class FallThrough:
    target: int


@dataclass
class Stop:
    pass


Terminator = Union[FallThrough, Stop]


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
    instructions: List[Instruction]
    terminator: Terminator


@dataclass
class Unit:
    entry: int
    codeblocks: List[CodeBlock]
