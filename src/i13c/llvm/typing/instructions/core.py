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
ImmediateWidth = Kind[8, 16, 32, 64]
DisplacementWidth = Kind[0, 8, 32]
DisplacementDirection = Kind["forward", "backward", "none"]
MemoryWidth = Kind[8, 16, 32, 64]
RegisterWidth = Kind["low", "high", "8bit", "16bit", "32bit", "64bit"]


@dataclass(kw_only=True)
class Immediate:
    data: bytes
    width: ImmediateWidth

    @staticmethod
    def imm8(data: bytes) -> Immediate:
        assert len(data) == 1
        return Immediate(data=data, width=8)

    @staticmethod
    def imm16(data: bytes) -> Immediate:
        assert len(data) == 2
        return Immediate(data=data, width=16)

    @staticmethod
    def imm32(data: bytes) -> Immediate:
        assert len(data) == 4
        return Immediate(data=data, width=32)

    @staticmethod
    def imm64(data: bytes) -> Immediate:
        assert len(data) == 8
        return Immediate(data=data, width=64)

    @staticmethod
    def auto(data: bytes) -> Immediate:
        width = len(data) * 8
        assert width in (8, 16, 32, 64)
        return Immediate(data=data, width=width)

    def is_one(self) -> bool:
        return int.from_bytes(self.data, byteorder="big", signed=False) == 1

    def sign_bit(self) -> bool:
        return (self.data[0] & 0x80) == 0x80

    def __str__(self) -> str:
        return f"0x{self.data.hex()}"


class DisplacementImmediate(Protocol):
    @property
    def data(self) -> bytes: ...

    @property
    def width(self) -> ImmediateWidth: ...


class DisplacementSource(Protocol):
    @property
    def kind(self) -> Kind["forward", "backward"]: ...

    @property
    def value(self) -> DisplacementImmediate: ...


@dataclass(kw_only=True)
class Displacement:
    data: bytes
    width: DisplacementWidth
    direction: DisplacementDirection

    @staticmethod
    def none() -> Displacement:
        return Displacement(data=bytes(), width=0, direction="none")

    @staticmethod
    def auto(source: Union[bytes, Optional[DisplacementSource]]) -> Displacement:
        if isinstance(source, (bytes, bytearray)):
            width = len(source) * 8
            assert width in (8, 32)

            if len(source.strip(bytes([0x00]))) == 0:
                direction = "none"
            elif source[0] < 0x80:
                direction = "forward"
            else:
                direction = "backward"

            return Displacement(
                data=source,
                width=width,
                direction=direction,
            )

        if source is None:
            return Displacement.none()

        assert not isinstance(source, (memoryview))
        assert source.value.width in (8, 32)

        return Displacement(
            data=source.value.data,
            width=source.value.width,
            direction=source.kind,
        )

    def get_width(self) -> DisplacementWidth:
        if self.width == 0:
            return 0

        if self.width == 8 and self.data[0] == 0x00:
            return 0

        if self.width == 8:
            return 8

        if self.width == 32 and self.data == bytes(4):
            return 0

        return self.width

    def normalize(self, width: DisplacementWidth) -> bytes:
        val = int.from_bytes(self.data, byteorder="big", signed=False)
        hex = val.to_bytes(width // 8, byteorder="big", signed=False)

        return hex


    def __str__(self) -> str:
        match self.direction:
            case "forward":
                return f" + 0x{self.data.hex()}"
            case "backward":
                return f" - 0x{self.data.hex()}"
            case "none":
                return ""


@dataclass(kw_only=True)
class Register:
    id: int
    width: RegisterWidth

    @staticmethod
    def none() -> Register:
        return Register(id=16, width="8bit")

    @staticmethod
    def auto(name: Optional[str]) -> Register:
        if name is None:
            return Register.none()

        for parser in (
            Register.parse8,
            Register.parse16,
            Register.parse32,
            Register.parse64,
        ):
            try:
                return parser(name)
            except KeyError:
                continue

        raise ValueError(f"Register name {name} is not recognized as a valid register")

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

    def is_low8bit(self) -> bool:
        return self.width == "low"

    def is_8bit(self) -> bool:
        return self.width in ("low", "high", "8bit")

    def is_16bit(self) -> bool:
        return self.width == "16bit"

    def is_32bit(self) -> bool:
        return self.width == "32bit"

    def is_64bit(self) -> bool:
        return self.width == "64bit"

    def is_acc(self) -> bool:
        return self.id == 0

    def get_width(self) -> Kind[8, 16, 32, 64]:
        if self.width == "64bit":
            return 64
        if self.width == "32bit":
            return 32
        if self.width == "16bit":
            return 16
        return 8

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

    @staticmethod
    def auto(index: Optional[str], scale: Optional[ScaleValue]) -> Scaler:
        return (
            Scaler(index=Register.auto(index), scale=scale)
            if scale is not None
            else Scaler.none()
        )

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
    width: MemoryWidth

    def __str__(self) -> str:
        return f"[{self.base}{self.scaler}{self.disp}]"


@dataclass(kw_only=True)
class RelativeAddress:
    disp: Displacement
    width: MemoryWidth

    def __str__(self) -> str:
        return f"[rip{self.disp}]"


Address = Union[ComputedAddress, RelativeAddress]
