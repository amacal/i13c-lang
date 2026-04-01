from dataclasses import dataclass

from i13c.llvm.typing.registers import reg64_to_name


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
