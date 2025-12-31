from dataclasses import dataclass
from typing import Literal as Kind
from typing import Tuple

Width = Kind[8, 16, 32, 64]


@dataclass(kw_only=True)
class Identifier:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Type:
    name: bytes
    width: Width
    lower: int
    upper: int

    def __str__(self) -> str:
        return f"{self.name.decode()}[{self.lower}..{self.upper}]"


def derive_width(value: int) -> Width:
    if value.bit_length() <= 8:
        return 8

    if value.bit_length() <= 16:
        return 16

    if value.bit_length() <= 32:
        return 32

    # we prevent integers larger than 64 bits
    return 64


def default_width(name: bytes) -> Width:
    if name == b"u8":
        return 8
    if name == b"u16":
        return 16
    if name == b"u32":
        return 32
    if name == b"u64":
        return 64

    assert False, f"Unknown type name: {name.decode()}"


def default_ranges(name: bytes) -> Tuple[int, int]:
    if name == b"u8":
        return (0, 0xFF)
    if name == b"u16":
        return (0, 0xFFFF)
    if name == b"u32":
        return (0, 0xFFFFFFFF)
    if name == b"u64":
        return (0, 0xFFFFFFFFFFFFFFFF)

    assert False, f"Unknown type name: {name.decode()}"
