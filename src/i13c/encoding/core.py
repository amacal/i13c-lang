from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class REX:
    w: bool
    r: bool
    x: bool
    b: bool

    def to_byte(self) -> int:
        value = 0x40

        if self.w:
            value |= 0x08

        if self.r:
            value |= 0x04

        if self.x:
            value |= 0x02

        if self.b:
            value |= 0x01

        return value


@dataclass(kw_only=True)
class Opcode:
    hex: int
    reg: Optional[int]

    def rex_b(self) -> bool:
        return ((self.reg & 0x08) == 0x08) if self.reg is not None else False

    def low_reg_bits(self) -> int:
        return self.reg & 0x07 if self.reg is not None else 0

    def to_byte(self) -> int:
        return self.hex | self.low_reg_bits()


@dataclass(kw_only=True)
class ModRM:
    mod: int
    reg: int
    rm: int

    def rex_r(self) -> bool:
        return ((self.reg >> 3) & 0x1) == 0x01

    def rex_b(self) -> bool:
        return ((self.rm >> 3) & 0x1) == 0x01

    def to_byte(self) -> int:
        return ((self.mod & 0x03) << 6) | ((self.reg & 0x07) << 3) | (self.rm & 0x07)


@dataclass(kw_only=True)
class SIB:
    base: int
    scale: int
    index: Optional[int]

    def rex_x(self) -> bool:
        return self.index is not None and ((self.index >> 3) & 0x1) == 0x1

    def rex_b(self) -> bool:
        return ((self.base >> 3) & 0x1) == 0x01

    def is_required(self) -> bool:
        return (self.base & 0x07) == 0x04 or self.index is not None

    def mod_rm(self) -> int:
        return 0x04 if self.is_required() else self.base & 0x07

    def to_bytes(self) -> bytes:
        if not self.is_required():
            return bytes([])

        if self.index is None:
            index_bits = 0b100
            scale_bits = 0
        else:
            index_bits = self.index & 0x07
            scale_bits = self.scale & 0x03

        return bytes([(scale_bits << 6) | (index_bits << 3) | (self.base & 0x07)])


@dataclass(kw_only=True)
class Immediate:
    value: int
    width: int
    signed: bool

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(self.width, byteorder="little", signed=self.signed)
