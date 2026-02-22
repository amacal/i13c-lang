from dataclasses import dataclass
from typing import Tuple, Union

from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.registers import IR_REGISTER_BACKWARD


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"mov {IR_REGISTER_BACKWARD[self.dst].decode()}, {self.imm:#010x}"


@dataclass(kw_only=True)
class MovRegReg:
    dst: int
    src: int

    def native(self) -> str:
        src = IR_REGISTER_BACKWARD[self.src].decode()
        dst = IR_REGISTER_BACKWARD[self.dst].decode()

        return f"mov {dst}, {src}"


@dataclass(kw_only=True)
class MovOffReg:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        src = IR_REGISTER_BACKWARD[self.src].decode()
        dst = IR_REGISTER_BACKWARD[self.dst].decode()
        sign = "+" if self.off >= 0 else "-"

        return f"mov {dst}, [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class MovRegOff:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        dst = IR_REGISTER_BACKWARD[self.dst].decode()
        src = IR_REGISTER_BACKWARD[self.src].decode()
        sign = "+" if self.off >= 0 else "-"

        return f"mov {dst}, [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class ShlRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {IR_REGISTER_BACKWARD[self.dst].decode()}, {self.imm:#010x}"


@dataclass(kw_only=True)
class SubRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"sub {IR_REGISTER_BACKWARD[self.dst].decode()}, {self.imm:#010x}"


@dataclass(kw_only=True)
class AddRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"add {IR_REGISTER_BACKWARD[self.dst].decode()}, {self.imm:#010x}"


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


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


InstructionEntry = Tuple[InstructionId, Instruction]
