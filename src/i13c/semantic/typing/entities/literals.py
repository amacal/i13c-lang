from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.core import Hex, Type
from i13c.syntax.source import Span

LiteralKind = Kind[b"hex"]


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("literal", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Literal:
    ref: Span
    kind: LiteralKind
    target: Hex

    def __str__(self) -> str:
        return f"kind={self.kind.decode()} {self.target}"

    def fits(self, type: Type) -> bool:
        if self.kind == b"hex":
            # width constraint
            if self.target.width != type.width:
                return False

            # lower bound constraint
            if Hex.lesser(self.target.data, type.range.lower.data):
                return False

            # upper bound constraint
            if Hex.greater(self.target.data, type.range.upper.data):
                return False

            # success
            return True

        return False
