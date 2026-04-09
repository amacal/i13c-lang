from dataclasses import dataclass
from typing import Literal as Kind

Width = Kind[8, 16, 32, 64]


@dataclass(kw_only=True, frozen=True)
class Identifier:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True, frozen=True)
class Hex:
    data: bytes
    width: Width

    @staticmethod
    def derive(data: bytes) -> Hex:
        width = len(data) * 8
        assert width in (8, 16, 32, 64)
        return Hex(data=data, width=width)

    @staticmethod
    def greater(left: bytes, right: bytes) -> bool:
        return int.from_bytes(left, byteorder="big", signed=False) > int.from_bytes(
            right, byteorder="big", signed=False
        )

    @staticmethod
    def lesser(left: bytes, right: bytes) -> bool:
        return int.from_bytes(left, byteorder="big", signed=False) < int.from_bytes(
            right, byteorder="big", signed=False
        )

    @staticmethod
    def max(left: Hex, right: Hex) -> Hex:
        return left if Hex.greater(left.data, right.data) else right

    @staticmethod
    def min(left: Hex, right: Hex) -> Hex:
        return left if Hex.lesser(left.data, right.data) else right

    def __str__(self) -> str:
        return f"0x{self.data.hex()}"


@dataclass(kw_only=True, frozen=True)
class Range:
    lower: Hex
    upper: Hex

    def __str__(self) -> str:
        return f"{self.lower}..{self.upper}"

    @staticmethod
    def intersection(left: Range, right: Range) -> Range:
        return Range(
            lower=Hex.max(left.lower, right.lower),
            upper=Hex.min(left.upper, right.upper),
        )


@dataclass(kw_only=True, frozen=True)
class Type:
    name: bytes
    width: Width
    range: Range

    def __str__(self) -> str:
        return f"{self.name.decode()}[{self.range}]"

    def accepts(self, other: Type) -> bool:
        return (
            self.width == other.width
            and Hex.max(self.range.lower, other.range.lower) == self.range.lower
            and Hex.min(self.range.upper, other.range.upper) == self.range.upper
        )


# def derive_width(value: int) -> Width:
#     if value < 0:
#         raise ValueError("Cannot derive width for negative values")

#     if value > 0xFFFF_FFFF_FFFF_FFFF:
#         raise ValueError("Cannot derive width for values larger than u64")

#     if value.bit_length() <= 8:
#         return 8

#     if value.bit_length() <= 16:
#         return 16

#     if value.bit_length() <= 32:
#         return 32

#     # we prevent integers larger than 64 bits
#     return 64


def default_width(name: bytes) -> Width:
    if name == b"u8":
        return 8
    if name == b"u16":
        return 16
    if name == b"u32":
        return 32
    if name == b"u64":
        return 64

    raise ValueError(f"Unknown type name: {name.decode()}")


def default_range(name: bytes) -> Range:
    if name == b"u8":
        return Range(
            lower=Hex(data=bytes([0x00] * 1), width=8),
            upper=Hex(data=bytes([0xFF] * 1), width=8),
        )

    if name == b"u16":
        return Range(
            lower=Hex(data=bytes([0x00] * 2), width=16),
            upper=Hex(data=bytes([0xFF] * 2), width=16),
        )

    if name == b"u32":
        return Range(
            lower=Hex(data=bytes([0x00] * 4), width=32),
            upper=Hex(data=bytes([0xFF] * 4), width=32),
        )

    if name == b"u64":
        return Range(
            lower=Hex(data=bytes([0x00] * 8), width=64),
            upper=Hex(data=bytes([0xFF] * 8), width=64),
        )

    raise ValueError(f"Unknown type name: {name.decode()}")


# def width_from_range(range: Range) -> Width:
#     return derive_width(range.upper)
