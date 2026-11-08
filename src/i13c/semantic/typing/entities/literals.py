from dataclasses import dataclass

from i13c.semantic.core import Hex, Type
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Literal:
    ref: Span
    target: Hex

    def __str__(self) -> str:
        return f"{self.target}"

    def fits(self, type: Type) -> bool:
        return False
