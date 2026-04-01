from dataclasses import dataclass

from i13c.llvm.typing.registers import reg32_to_name, reg64_to_name


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
