from collections.abc import Callable, Iterable, Sequence
from typing import Any, Literal as Kind

from pytest import mark

from i13c.encoding import DISPATCH_TABLE
from i13c.encoding.core import UnreachableEncodingError
from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.blocklets import BlockletInstruction
from i13c.semantic.typing.analyses.llvm import (
    Address,
    Fixed,
    Immediate,
    Index,
    Register,
    Displacement,
)


def parse_value(header: str, value: str) -> str | int | bytes | None:
    if not value.strip(" -"):
        return None

    if header in ("scale"):
        return int(value, 16)

    if header in ("imm", "imm8", "imm32", "imm64", "disp8", "disp32"):
        return bytes.fromhex(value[2:])

    return value


def parse_encoding(value: str) -> bytes | None:
    return bytes.fromhex(value) if "!" not in value else None


def parse_samples(
    table: str,
) -> tuple[Sequence[str], Iterable[Sequence[int | str | bytes | None]]]:
    rows: list[Sequence[int | str | bytes | None]] = []
    lines = [line.strip("|\n ") for line in table.splitlines()[2:-1]]
    headers = [h.strip().lower() for h in lines[0].split("|")]

    try:
        separator = headers.index("***")
    except ValueError:
        separator = len(headers)

    for line in [line for line in lines[2:-1] if "---" not in line]:
        parts = [p.strip() for p in line.split("|")]
        left, right = parts[:separator], parts[separator + 1 :]

        rows.append(
            [parse_value(headers[i], left[i]) for i in range(separator - 1)]
            + [parse_encoding(left[separator - 1])]
        )

        if separator < len(parts):
            rows.append(
                [parse_value(headers[i], right[i]) for i in range(separator - 1)]
                + [parse_encoding(right[separator - 1])]
            )

    return (headers[:separator], rows)


def samples(table: str):
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        headers, cases = parse_samples(table)
        return mark.parametrize(",".join(headers), cases)(fn)

    return wrapper


class RegisterInfo:
    @staticmethod
    def auto(name: str) -> Register:
        return Register(name=name.encode("utf-8"))

    @staticmethod
    def optional(name: str | None) -> Register | None:
        return RegisterInfo.auto(name) if name is not None else None


class ImmediateInfo:
    @staticmethod
    def auto(value: bytes) -> Immediate:
        return Immediate(value=Hex.derive(value))


class IndexInfo:
    @staticmethod
    def optional(reg: str | None, scale: Kind[1, 2, 4, 8] | None) -> Index | None:
        return (
            Index(reg=RegisterInfo.auto(reg), scale=scale)
            if reg is not None and scale is not None
            else None
        )

class DisplacementInfo:
    @staticmethod
    def auto(value: bytes | None) -> Displacement | None:
        return Displacement.positive(int.from_bytes(value, "big")) if value and len(value.strip(bytes([0x00]))) else None


def parse_address(
    base: str | None,
    scale: Kind[1, 2, 4, 8] | None,
    index: str | None,
    disp32: bytes | None,
) -> Address | Fixed:

    if base == "rip" and scale is None and index is None and disp32 is not None:
        return Fixed(value=disp32)

    return Address(
        size=64,
        base=RegisterInfo.optional(base),
        indx=IndexInfo.optional(index, scale),
        disp=DisplacementInfo.auto(disp32),
    )


def encode_instruction(
    instruction: BlockletInstruction, encoding: bytes | None
) -> None:
    try:
        bytes = bytearray()
        DISPATCH_TABLE[type(instruction)](instruction, bytes)

        assert encoding is not None
        assert bytes.hex(" ") == encoding.hex(" ")
    except UnreachableEncodingError:
        assert encoding is None
