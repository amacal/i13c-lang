from dataclasses import dataclass

from i13c.llvm.typing.instructions.core import ComputedAddress, Immediate
from i13c.llvm.typing.registers import reg64_to_name


@dataclass(kw_only=True)
class MovRegImm:
    dst: int
    imm: Immediate

    def native(self) -> str:
        return f"mov {reg64_to_name(self.dst)}, {self.imm}"


@dataclass(kw_only=True)
class MovOffImm:
    dst: ComputedAddress
    imm: Immediate

    def native(self) -> str:
        return f"mov {self.dst}, {self.imm}"


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
    dst: ComputedAddress
    src: int

    def native(self) -> str:
        return f"mov {self.dst}, {reg64_to_name(self.src)}"


@dataclass(kw_only=True)
class MovRegOff:
    dst: int
    src: ComputedAddress

    def native(self) -> str:
        return f"mov {reg64_to_name(self.dst)}, {self.src}"
