from typing import Any, Callable, Iterable, List, Sequence, Tuple, Union

from pytest import mark


def parse_value(header: str, value: str) -> Union[str, int]:
    return (
        int(value, 16)
        if header in ("imm8", "imm32", "imm64", "disp8", "disp32")
        else value
    )


def parse_samples(
    table: str,
) -> Tuple[Sequence[str], Iterable[Sequence[Union[int, str, bytes]]]]:
    rows: List[Sequence[Union[int, str, bytes]]] = []
    lines = [line.strip("|\n ") for line in table.splitlines()[2:-1]]

    headers = [h.strip().lower() for h in lines[0].split("|")]
    separator = headers.index("*")

    for line in [line for line in lines[2:-1] if "-" not in line]:
        parts = [p.strip() for p in line.split("|")]
        left, right = parts[:separator], parts[separator + 1 :]

        rows.append(
            [parse_value(headers[i], left[i]) for i in range(separator - 1)]
            + [bytes.fromhex(left[separator - 1])]
        )

        rows.append(
            [parse_value(headers[i], right[i]) for i in range(separator - 1)]
            + [bytes.fromhex(right[separator - 1])]
        )

    return (headers[:separator], rows)


def samples(table: str):
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        headers, cases = parse_samples(table)
        return mark.parametrize(",".join(headers), cases)(fn)

    return wrapper
