from dataclasses import dataclass
from typing import Dict, Union

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


@dataclass(kw_only=True)
class EnterFrame:
    size: int


@dataclass(kw_only=True)
class ExitFrame:
    size: int


@dataclass(kw_only=True)
class Preserve:
    registers: Dict[int, int]


@dataclass(kw_only=True)
class Restore:
    registers: Dict[int, int]


Instruction = Union[
    MovRegImm,
    MovOffReg,
    MovRegOff,
    ShlRegImm,
    SysCall,
    Label,
    Call,
    Return,
    Jump,
    EnterFrame,
    ExitFrame,
    Preserve,
    Restore,
]
