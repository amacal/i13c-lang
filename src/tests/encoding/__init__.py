from collections.abc import Callable, Iterable, Sequence
from typing import Any

from pytest import mark

from i13c.encoding import encode
from i13c.encoding.core import UnreachableEncodingError
from i13c.llvm.typing.instructions import Instruction, core


def parse_value(header: str, value: str) -> str | int | bytes | None:
    if not value.strip(" -"):
        return None

    if header in ("scale"):
        return int(value, 16)

    if header in ("imm8", "imm32", "imm64", "disp8", "disp32"):
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


def parse_address(
    base: str | None,
    scale: core.ScaleValue | None,
    index: str | None,
    disp32: bytes | None,
) -> core.ComputedAddress | core.RelativeAddress:

    if base == "rip" and scale is None and index is None:
        return core.RelativeAddress(
            disp=core.Displacement.auto(disp32),
            width=64,
        )

    return core.ComputedAddress(
        base=core.Register.auto(base),
        disp=core.Displacement.auto(disp32),
        scaler=core.Scaler.auto(index, scale),
        width=64,
    )


def encode_instruction(instruction: Instruction, encoding: bytes | None) -> None:
    try:
        encoded = encode([instruction]).hex(" ")

        assert encoding is not None
        assert encoded == encoding.hex(" ")
    except UnreachableEncodingError:
        assert encoding is None
