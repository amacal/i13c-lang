from dataclasses import dataclass
from typing import Protocol


class SliceIndex(Protocol):
    offset: int
    length: int


@dataclass(kw_only=True)
class SourceCode:
    data: bytes

    def is_eof(self, offset: int) -> bool:
        return offset >= len(self.data)

    def at(self, offset: int) -> int:
        return self.data[offset]

    def extract(self, slice: SliceIndex) -> bytes:
        return self.data[slice.offset : slice.offset + slice.length]


def open_text(data: str) -> SourceCode:
    return SourceCode(data=data.encode("utf-8"))
