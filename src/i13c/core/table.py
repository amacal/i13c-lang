from typing import Callable, Dict, Iterable, List, TypeVar

DrawItem = TypeVar("DrawItem")
DrawCallback = Callable[[DrawItem], str]


class Table:
    def __init__(self, entries: List[str]):
        self.entries = entries

    def reformat(self) -> List[str]:
        return [
            line.replace("-+-", " | ").replace("+-", "| ").replace("-+", " |")
            for line in self.entries
        ]

    def equals(self, other: str) -> None:
        assert "\n".join(self.reformat()) == "\n".join(
            line.strip() for line in other.strip().splitlines()
        )


def draw_table(headers: Dict[str, str], rows: List[Dict[str, str]]) -> Table:
    header_widths = measure_headers(headers)
    row_widths = measure_rows(headers, rows)

    widths = {key: max(header_widths[key], row_widths[key]) for key in headers}

    return Table(
        [
            draw_separator(widths.values()),
            draw_header(widths.values(), headers),
            draw_separator(widths.values()),
            *[draw_row(widths.values(), row) for row in rows],
            draw_separator(widths.values()),
        ]
    )


def measure_headers(headers: Dict[str, str]) -> Dict[str, int]:
    return {key: len(value) for key, value in headers.items()}


def measure_rows(headers: Dict[str, str], rows: List[Dict[str, str]]) -> Dict[str, int]:
    return {key: max(len(row[key]) for row in rows) if rows else 0 for key in headers}


def draw_separator(widths: Iterable[int]) -> str:
    return draw("+", widths, lambda width: "-" * (width + 2))


def draw_header(widths: Iterable[int], headers: Dict[str, str]) -> str:
    return draw("|", zip(headers, widths), lambda x: f" {headers[x[0]]:<{x[1]}} ")


def draw_row(widths: Iterable[int], row: Dict[str, str]) -> str:
    return draw("|", zip(row, widths), lambda x: f" {row[x[0]]:<{x[1]}} ")


def draw(sep: str, items: Iterable[DrawItem], callback: DrawCallback[DrawItem]) -> str:
    return sep + sep.join(callback(item) for item in items) + sep
