from dataclasses import dataclass
from typing import Literal as Kind
from typing import Optional

Width = Kind[8, 16, 32, 64]


@dataclass(kw_only=True)
class Identifier:
    name: bytes


@dataclass(kw_only=True)
class Type:
    name: bytes


def derive_width(value: int) -> Optional[Width]:
    if value.bit_length() <= 8:
        return 8

    if value.bit_length() <= 16:
        return 16

    if value.bit_length() <= 32:
        return 32

    if value.bit_length() <= 64:
        return 64

    return None
