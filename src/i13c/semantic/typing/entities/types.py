from dataclasses import dataclass
from typing import Optional

from i13c.semantic.typing.entities.ranges import RangeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class TypeId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("type", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Type:
    ref: Span
    name: bytes
    range: Optional[RangeId]

    def __str__(self) -> str:
        return (
            f"{self.name.decode()}[{self.range.identify(1)}]"
            if self.range is not None
            else f"{self.name.decode()}"
        )
