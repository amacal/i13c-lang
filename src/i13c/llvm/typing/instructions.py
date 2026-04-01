from dataclasses import dataclass
from typing import Tuple, Union

from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.registers import reg32_to_name, reg64_to_name


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"mov {reg64_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class MovOffImm:
    dst: int
    imm: int
    off: int

    def native(self) -> str:
        dst = reg64_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"
        return f"mov [{dst} {sign} {abs(self.off):#010x}], {self.imm:#010x}"


@dataclass(kw_only=True)
class MovRegReg:
    dst: int
    src: int

    def native(self) -> str:
        src = reg64_to_name(self.src)
        dst = reg64_to_name(self.dst)

        return f"mov {dst}, {src}"


@dataclass(kw_only=True)
class MovOffReg:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        src = reg64_to_name(self.src)
        dst = reg64_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"

        return f"mov [{dst} {sign} {abs(self.off):#010x}], {src}"


@dataclass(kw_only=True)
class MovRegOff:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        dst = reg64_to_name(self.dst)
        src = reg64_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"mov {dst}, [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class PushOff:
    src: int
    off: int

    def native(self) -> str:
        src = reg64_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"push [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class PopOff:
    dst: int
    off: int

    def native(self) -> str:
        dst = reg64_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"

        return f"pop [{dst} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class ShlRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {reg64_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class ShlRegReg:
    dst: int

    def native(self) -> str:
        return f"shl {reg64_to_name(self.dst)}, cl"


@dataclass(kw_only=True)
class SubRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"sub {reg64_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class AddRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"add {reg64_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class AddRegReg:
    dst: int
    src: int

    def native(self) -> str:
        return f"add {reg64_to_name(self.dst)}, {reg64_to_name(self.src)}"


@dataclass(kw_only=True)
class LeaRegOff:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        dst = reg64_to_name(self.dst)
        src = reg64_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"lea {dst}, [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class ByteSwapReg32:
    target: int

    def native(self) -> str:
        return f"bswap {reg32_to_name(self.target)}"


@dataclass(kw_only=True)
class ByteSwapReg64:
    target: int

    def native(self) -> str:
        return f"bswap {reg64_to_name(self.target)}"


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
    AddRegImm,
    AddRegReg,
    ByteSwapReg32,
    ByteSwapReg64,
    Call,
    Jump,
    Label,
    LeaRegOff,
    MovOffImm,
    MovOffReg,
    MovRegImm,
    MovRegOff,
    MovRegReg,
    Nop,
    PopOff,
    PushOff,
    Return,
    ShlRegImm,
    ShlRegReg,
    SubRegImm,
    SysCall,
]


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


InstructionEntry = Tuple[InstructionId, Instruction]
