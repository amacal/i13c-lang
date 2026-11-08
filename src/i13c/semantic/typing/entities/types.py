from dataclasses import dataclass

from i13c.semantic.typing.identifiers.ranges import RangeId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Type:
    ref: Span
    name: bytes
    range: RangeId | None

    def __str__(self) -> str:
        return (
            f"{self.name.decode()}[{self.range.identify(1)}]"
            if self.range is not None
            else f"{self.name.decode()}"
        )
