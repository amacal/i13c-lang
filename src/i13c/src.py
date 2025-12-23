from dataclasses import dataclass
from typing import Protocol


@dataclass
class Span:
    offset: int
    length: int


class SpanLike(Protocol):
    offset: int
    length: int


@dataclass(kw_only=True)
class SourceCode:
    data: bytes

    def is_eof(self, offset: int) -> bool:
        return offset >= len(self.data)

    def at(self, offset: int) -> int:
        return self.data[offset]

    def extract(self, span: SpanLike) -> bytes:
        return self.data[span.offset : span.offset + span.length]


def open_text(data: str) -> SourceCode:
    return SourceCode(data=data.encode("utf-8"))
