from dataclasses import dataclass
from typing import Union

from i13c.lowering.typing.flows import BlockId


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: int


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


Instruction = Union[MovRegImm, ShlRegImm, SysCall, Label, Call, Return]
