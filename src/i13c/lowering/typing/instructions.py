from dataclasses import dataclass
from typing import Tuple, Union

from i13c.lowering.typing.flows import BlockId


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: int

    def raw(self) -> Tuple[str, ...]:
        return ("MovRegImm", str(self.dst), str(self.imm))


@dataclass(kw_only=True)
class MovRegReg:
    dst: int
    src: int

    def raw(self) -> Tuple[str, ...]:
        return ("MovRegReg", str(self.dst), str(self.src))


@dataclass(kw_only=True)
class MovOffReg:
    dst: int
    src: int
    off: int

    def raw(self) -> Tuple[str, ...]:
        return ("MovOffReg", str(self.dst), str(self.src), str(self.off))


@dataclass(kw_only=True)
class MovRegOff:
    dst: int
    src: int
    off: int

    def raw(self) -> Tuple[str, ...]:
        return ("MovRegOff", str(self.dst), str(self.src), str(self.off))


@dataclass(kw_only=True)
class ShlRegImm:
    dst: int
    imm: int

    def raw(self) -> Tuple[str, ...]:
        return ("ShlRegImm", str(self.dst), str(self.imm))


@dataclass(kw_only=True)
class SubRegImm:
    dst: int
    imm: int

    def raw(self) -> Tuple[str, ...]:
        return ("SubRegImm", str(self.dst), str(self.imm))


@dataclass(kw_only=True)
class AddRegImm:
    dst: int
    imm: int

    def raw(self) -> Tuple[str, ...]:
        return ("AddRegImm", str(self.dst), str(self.imm))


@dataclass(kw_only=True)
class SysCall:
    def raw(self) -> Tuple[str, ...]:
        return ("SysCall",)


@dataclass(kw_only=True)
class Call:
    target: BlockId

    def raw(self) -> Tuple[str, ...]:
        return ("Call", str(self.target.value))


@dataclass(kw_only=True)
class Label:
    id: BlockId

    def raw(self) -> Tuple[str, ...]:
        return ("Label", str(self.id.value))


@dataclass(kw_only=True)
class Return:
    def raw(self) -> Tuple[str, ...]:
        return ("Return",)


@dataclass(kw_only=True)
class Jump:
    target: BlockId

    def raw(self) -> Tuple[str, ...]:
        return ("Jump", str(self.target.value))


Instruction = Union[
    MovRegImm,
    MovRegReg,
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
