from dataclasses import dataclass

from i13c.llvm.typing.registers import reg64_to_name


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
