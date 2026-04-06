from typing import Any, Callable, Iterable, List, Optional, Sequence, Tuple, Union

from pytest import mark


def parse_value(header: str, value: str) -> Union[str, int]:
    if header in ("imm8", "imm32", "imm64", "scale"):
        return int(value, 16)

    if header == "disp8":
        x = int(value, 16)
        return x if x < 0x80 else x - 0x100

    if header == "disp32":
        x = int(value, 16)
        return x if x < 0x80000000 else x - 0x100000000

    return value


def parse_encoding(value: str) -> Optional[bytes]:
    return bytes.fromhex(value) if "!" not in value else None


def parse_samples(
    table: str,
) -> Tuple[Sequence[str], Iterable[Sequence[Union[int, str, Optional[bytes]]]]]:
    rows: List[Sequence[Union[int, str, Optional[bytes]]]] = []
    lines = [line.strip("|\n ") for line in table.splitlines()[2:-1]]
    headers = [h.strip().lower() for h in lines[0].split("|")]

    try:
        separator = headers.index("***")
    except ValueError:
        separator = len(headers)

    for line in [line for line in lines[2:-1] if "-" not in line]:
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
