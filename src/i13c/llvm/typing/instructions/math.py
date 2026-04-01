from dataclasses import dataclass

from i13c.llvm.typing.registers import reg64_to_name


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
class SubRegImm:
    dst: int
    imm: int

    def native(self) -> str:
        return f"sub {reg64_to_name(self.dst)}, {self.imm:#010x}"
