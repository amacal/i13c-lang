from dataclasses import dataclass
from typing import Tuple, Union

from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.registers import reg_to_name


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"mov {reg_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class MovOffImm:
    dst: int
    imm: int
    off: int

    def native(self) -> str:
        dst = reg_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"
        return f"mov [{dst} {sign} {abs(self.off):#010x}], {self.imm:#010x}"


@dataclass(kw_only=True)
class MovRegReg:
    dst: int
    src: int

    def native(self) -> str:
        src = reg_to_name(self.src)
        dst = reg_to_name(self.dst)

        return f"mov {dst}, {src}"


@dataclass(kw_only=True)
class MovOffReg:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        src = reg_to_name(self.src)
        dst = reg_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"

        return f"mov [{dst} {sign} {abs(self.off):#010x}], {src}"


@dataclass(kw_only=True)
class MovRegOff:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        dst = reg_to_name(self.dst)
        src = reg_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"mov {dst}, [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class PushOff:
    src: int
    off: int

    def native(self) -> str:
        src = reg_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"push [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class PopOff:
    dst: int
    off: int

    def native(self) -> str:
        dst = reg_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"

        return f"pop [{dst} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class ShlRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {reg_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class SubRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"sub {reg_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class AddRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"add {reg_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class SysCall:
    def native(self) -> str:
        return "syscall"


@dataclass(kw_only=True)
class Call:
    target: BlockId

    def native(self) -> str:
        return f"call {self.target.identify(1)}"


@dataclass(kw_only=True)
class Label:
    id: BlockId

    def native(self) -> str:
        return f"label {self.id.identify(1)}"


@dataclass(kw_only=True)
class Return:
    def native(self) -> str:
        return "ret"


@dataclass(kw_only=True)
class Jump:
    target: BlockId

    def native(self) -> str:
        return f"jmp {self.target.identify(1)}"


@dataclass(kw_only=True)
class Nop:
    def native(self) -> str:
        return "nop"


Instruction = Union[
    MovRegImm,
    MovRegReg,
    MovOffImm,
    MovOffReg,
    MovRegOff,
    ShlRegImm,
    SubRegImm,
    AddRegImm,
    PushOff,
    PopOff,
    SysCall,
    Label,
    Call,
    Return,
    Jump,
    Nop,
]


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


InstructionEntry = Tuple[InstructionId, Instruction]
