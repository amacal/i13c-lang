from dataclasses import dataclass
from typing import Union

from i13c.llvm.typing.instructions.core import Immediate, Register


@dataclass(kw_only=True)
class ByteSwapReg32:
    dst: Register

    def native(self) -> str:
        return f"bswap {self.dst}"


@dataclass(kw_only=True)
class ByteSwapReg64:
    dst: Register

    def native(self) -> str:
        return f"bswap {self.dst}"


@dataclass(kw_only=True)
class ShlReg8Imm8:
    dst: Register
    imm: Immediate

    def native(self) -> str:
        return f"shl {self.dst}, {self.imm}"


@dataclass(kw_only=True)
class ShlReg16Imm8:
    dst: Register
    imm: Immediate

    def native(self) -> str:
        return f"shl {self.dst}, {self.imm}"


@dataclass(kw_only=True)
class ShlReg32Imm8:
    dst: Register
    imm: Immediate

    def native(self) -> str:
        return f"shl {self.dst}, {self.imm}"


@dataclass(kw_only=True)
class ShlReg64Imm8:
    dst: Register
    imm: Immediate

    def native(self) -> str:
        return f"shl {self.dst}, {self.imm}"


@dataclass(kw_only=True)
class ShlReg8Cl:
    dst: Register

    def native(self) -> str:
        return f"shl {self.dst}, cl"


@dataclass(kw_only=True)
class ShlReg16Cl:
    dst: Register

    def native(self) -> str:
        return f"shl {self.dst}, cl"


@dataclass(kw_only=True)
class ShlReg32Cl:
    dst: Register

    def native(self) -> str:
        return f"shl {self.dst}, cl"


@dataclass(kw_only=True)
class ShlReg64Cl:
    dst: Register

    def native(self) -> str:
        return f"shl {self.dst}, cl"


BSwapReg = Union[ByteSwapReg32, ByteSwapReg64]

ShlRegImm = Union[
    ShlReg8Imm8,
    ShlReg16Imm8,
    ShlReg32Imm8,
    ShlReg64Imm8,
]

ShlRegReg = Union[
    ShlReg8Cl,
    ShlReg16Cl,
    ShlReg32Cl,
    ShlReg64Cl,
]
