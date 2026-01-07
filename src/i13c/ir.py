from dataclasses import dataclass
from typing import Union


@dataclass
class FallThrough:
    pass


@dataclass
class Stop:
    pass


@dataclass
class Emit:
    pass


Terminator = Union[FallThrough, Stop, Emit]


@dataclass
class MovRegImm:
    dst: int
    imm: int


@dataclass
class ShlRegImm:
    dst: int
    imm: int


@dataclass
class SysCall:
    pass


Instruction = Union[MovRegImm, ShlRegImm, SysCall]


@dataclass
class Label:
    id: int


@dataclass
class Jump:
    label: int


InstructionFlow = Union[Instruction, Label, Jump]
