from dataclasses import dataclass

from i13c.llvm.typing.registers import reg64_to_name


@dataclass(kw_only=True)
class PopOff:
    dst: int
    off: int

    def native(self) -> str:
        dst = reg64_to_name(self.dst)
        sign = "+" if self.off >= 0 else "-"

        return f"pop [{dst} {sign} {abs(self.off):#010x}]"


@dataclass(kw_only=True)
class PushOff:
    src: int
    off: int

    def native(self) -> str:
        src = reg64_to_name(self.src)
        sign = "+" if self.off >= 0 else "-"

        return f"push [{src} {sign} {abs(self.off):#010x}]"
