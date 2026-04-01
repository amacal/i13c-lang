from dataclasses import dataclass

from i13c.llvm.typing.registers import (
    reg8_to_name,
    reg16_to_name,
    reg32_to_name,
    reg64_to_name,
)


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
class ShlReg8Imm8:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {reg8_to_name(self.dst)}, {self.imm:#04x}"


@dataclass(kw_only=True)
class ShlReg16Imm8:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {reg16_to_name(self.dst)}, {self.imm:#04x}"


@dataclass(kw_only=True)
class ShlReg32Imm8:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {reg32_to_name(self.dst)}, {self.imm:#04x}"


@dataclass(kw_only=True)
class ShlReg64Imm8:
    dst: int
    imm: int

    def native(self) -> str:
        return f"shl {reg64_to_name(self.dst)}, {self.imm:#04x}"


@dataclass(kw_only=True)
class ShlReg32Cl:
    dst: int

    def native(self) -> str:
        return f"shl {reg32_to_name(self.dst)}, cl"


@dataclass(kw_only=True)
class ShlReg64Cl:
    dst: int

    def native(self) -> str:
        return f"shl {reg64_to_name(self.dst)}, cl"
