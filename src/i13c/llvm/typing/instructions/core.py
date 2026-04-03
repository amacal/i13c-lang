from dataclasses import dataclass
from typing import Literal as Kind

from i13c.llvm.typing.registers import (
    name_to_reg32,
    name_to_reg64,
    reg8_to_name,
    reg16_to_name,
    reg32_to_name,
    reg64_to_name,
)

ImmediateWidth = Kind[8, 32, 64]
RegisterWidth = Kind[8, 16, 32, 64]
DisplacementWidth = Kind[0, 8, 32]


@dataclass(kw_only=True)
class Immediate:
    value: int
    width: ImmediateWidth

    @staticmethod
    def imm8(value: int) -> Immediate:
        return Immediate(value=value, width=8)

    @staticmethod
    def imm32(value: int) -> Immediate:
        return Immediate(value=value, width=32)

    @staticmethod
    def imm64(value: int) -> Immediate:
        return Immediate(value=value, width=64)


@dataclass(kw_only=True)
class Displacement:
    value: int
    width: DisplacementWidth

    @staticmethod
    def auto(value: int) -> Displacement:
        if value == 0:
            return Displacement(value=value, width=0)

        if -128 <= value <= 127:
            return Displacement(value=value, width=8)

        if -(2**31) <= value <= 2**31 - 1:
            return Displacement(value=value, width=32)

        raise ValueError(
            f"Displacement value {value} is out of range for 32-bit signed integer"
        )

    def __str__(self) -> str:
        return f"{'+' if self.value >= 0 else '-'} {abs(self.value):#010x}"


@dataclass(kw_only=True)
class Register:
    id: int
    width: RegisterWidth

    @staticmethod
    def reg32(id: int) -> Register:
        return Register.build(32, id)

    @staticmethod
    def parse32(name: str) -> Register:
        return Register.reg32(name_to_reg32(name))

    @staticmethod
    def reg64(id: int) -> Register:
        return Register.build(64, id)

    @staticmethod
    def parse64(name: str) -> Register:
        return Register.reg64(name_to_reg64(name))

    @staticmethod
    def build(width: RegisterWidth, id: int) -> Register:
        assert 0 <= id < 16, f"Register id {id} is out of range (0-15)"

        return Register(id=id, width=width)

    def __str__(self) -> str:
        if self.width == 8:
            return reg8_to_name(self.id)

        if self.width == 16:
            return reg16_to_name(self.id)

        if self.width == 32:
            return reg32_to_name(self.id)

        return reg64_to_name(self.id)


@dataclass(kw_only=True)
class Address:
    base: Register
    disp: Displacement

    def __str__(self) -> str:
        return f"[{self.base} {self.disp}]"
