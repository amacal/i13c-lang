from dataclasses import dataclass

from i13c.llvm.typing.registers import reg32_to_name, reg64_to_name


@dataclass(kw_only=True)
class LeaReg32Off:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        dst = reg32_to_name(self.dst)
        src = reg64_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"lea {dst}, [{src} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class LeaReg64Off:
    dst: int
    src: int
    off: int

    def native(self) -> str:
        dst = reg64_to_name(self.dst)
        src = reg64_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"lea {dst}, [{src} {sign} {abs(self.off):#010x}]"
