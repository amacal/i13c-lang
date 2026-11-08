from dataclasses import dataclass

from i13c.semantic.core import Hex
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Range:
    ref: Span
    lower: Hex
    upper: Hex

    def __str__(self) -> str:
        return f"{self.lower}..{self.upper}"
