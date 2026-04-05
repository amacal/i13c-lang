from dataclasses import dataclass
from typing import Literal as Kind
from typing import Optional, Protocol, Union

from i13c.llvm.typing.registers import (
    name_to_reg8,
    name_to_reg16,
    name_to_reg32,
    name_to_reg64,
    reg8_to_name,
    reg16_to_name,
    reg32_to_name,
    reg64_to_name,
)

ScaleValue = Kind[1, 2, 4, 8]
ImmediateWidth = Kind[8, 32, 64]
DisplacementWidth = Kind[0, 8, 32]
RegisterWidth = Kind["low", "high", "8bit", "16bit", "32bit", "64bit"]


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

    def __str__(self) -> str:
        if self.width == 8:
            return f"{self.value:#04x}"

        if self.width == 32:
            return f"{self.value:#010x}"

        return f"{self.value:#018x}"


class DisplacementSource(Protocol):
    @property
    def value(self) -> int: ...


@dataclass(kw_only=True)
class Displacement:
    value: int
    width: DisplacementWidth

    @staticmethod
    def none() -> Displacement:
        return Displacement(value=0, width=0)

    @staticmethod
    def auto(source: Union[int, Optional[DisplacementSource]]) -> Displacement:
        if isinstance(source, int):
            value = source
        else:
            value = source.value if source is not None else 0

        if value == 0:
            return Displacement.none()

        if -128 <= value <= 127:
            return Displacement(value=value, width=8)

        if -(2**31) <= value <= 2**31 - 1:
            return Displacement(value=value, width=32)

        raise ValueError(
            f"Displacement value {value} is out of range for 32-bit signed integer"
        )

    def __str__(self) -> str:
        return f" {'+' if self.value >= 0 else '-'} {abs(self.value):#010x}"


@dataclass(kw_only=True)
class Register:
    id: int
    width: RegisterWidth

    @staticmethod
    def none() -> Register:
        return Register(id=16, width="8bit")

    @staticmethod
    def reg8(id: int, width: Kind["low", "high", "8bit"]) -> Register:
        return Register.build(width, id)

    @staticmethod
    def parse8(name: str) -> Register:
        return Register.reg8(*name_to_reg8(name))

    @staticmethod
    def reg16(id: int) -> Register:
        return Register.build("16bit", id)

    @staticmethod
    def parse16(name: str) -> Register:
        return Register.reg16(name_to_reg16(name))

    @staticmethod
    def reg32(id: int) -> Register:
        return Register.build("32bit", id)

    @staticmethod
    def parse32(name: str) -> Register:
        return Register.reg32(name_to_reg32(name))

    @staticmethod
    def reg64(id: int) -> Register:
        return Register.build("64bit", id)

    @staticmethod
    def parse64(name: str) -> Register:
        return Register.reg64(name_to_reg64(name))

    @staticmethod
    def build(width: RegisterWidth, id: int) -> Register:
        assert 0 <= id < 16, f"Register id {id} is out of range (0-15)"

        return Register(id=id, width=width)

    def is_available(self) -> bool:
        return self.id != 16

    def value_or_none(self) -> Optional[int]:
        return self.id if self.is_available() else None

    def low3bits(self) -> int:
        return self.id & 0x07

    def high4bit(self) -> int:
        return self.id & 0x08

    def high_bit(self) -> bool:
        return ((self.id >> 3) & 0x01) == 0x01

    def is_64bit(self) -> bool:
        return self.width == "64bit"

    def __str__(self) -> str:
        if self.width in ("low", "high", "8bit"):
            return reg8_to_name(self.id)

        if self.width == "16bit":
            return reg16_to_name(self.id)

        if self.width == "32bit":
            return reg32_to_name(self.id)

        return reg64_to_name(self.id)


@dataclass(kw_only=True)
class Scaler:
    index: Register
    scale: ScaleValue

    @staticmethod
    def none() -> Scaler:
        return Scaler(index=Register.none(), scale=1)

    def is_available(self) -> bool:
        return self.index.is_available()

    def index_uses_rsp(self) -> bool:
        return self.index.id in (4,)

    def index_or_none(self) -> Optional[int]:
        return self.index.value_or_none()

    def scale_offset(self) -> int:
        return [1, 2, 4, 8].index(int(self.scale)) if self.is_available() else 0

    def __str__(self) -> str:
        return f" + {self.index}*{self.scale}" if self.is_available() else ""


@dataclass(kw_only=True)
class ComputedAddress:
    base: Register
    disp: Displacement
    scaler: Scaler

    def __str__(self) -> str:
        return f"[{self.base}{self.scaler}{self.disp}]"


@dataclass(kw_only=True)
class RelativeAddress:
    disp: Displacement

    def __str__(self) -> str:
        return f"[rip{self.disp}]"


Address = Union[ComputedAddress, RelativeAddress]

EncodingKind = Kind[
    "op",
    "op+imm",
    "op+reg",
    "op+reg+imm",
    "op+mod+reg",
    "op+mod+ext",
    "op+mod+reg+imm",
    "op+mod+ext+imm",
    "op+rel",
]
