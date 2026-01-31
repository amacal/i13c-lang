from dataclasses import dataclass
from typing import Union

from i13c.lowering.typing.flows import BlockId


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: int


@dataclass(kw_only=True)
class MovOffReg:
    dst: int
    src: int
    off: int


@dataclass(kw_only=True)
class MovRegOff:
    dst: int
    src: int
    off: int


@dataclass(kw_only=True)
class ShlRegImm:
    dst: int
    imm: int


@dataclass(kw_only=True)
class SubRegImm:
    dst: int
    imm: int


@dataclass(kw_only=True)
class AddRegImm:
    dst: int
    imm: int


@dataclass(kw_only=True)
class SysCall:
    pass


@dataclass(kw_only=True)
class Call:
    target: BlockId


@dataclass(kw_only=True)
class Label:
    id: BlockId


@dataclass(kw_only=True)
class Return:
    pass


@dataclass(kw_only=True)
class Jump:
    target: BlockId


Instruction = Union[
    MovRegImm,
    MovOffReg,
    MovRegOff,
    ShlRegImm,
    SubRegImm,
    AddRegImm,
    SysCall,
    Label,
    Call,
    Return,
    Jump,
]
