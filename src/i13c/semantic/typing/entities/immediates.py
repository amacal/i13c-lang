from dataclasses import dataclass

from i13c.semantic.core import Hex
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Immediate:
    ref: Span
    value: Hex

    def __str__(self) -> str:
        return f"{self.value}"
