from dataclasses import dataclass
from typing import Literal as Kind

from i13c.sem.core import Width
from i13c.src import Span

LiteralKind = Kind[b"hex"]


@dataclass(kw_only=True)
class Hex:
    value: int
    width: Width

    def describe(self) -> str:
        bytes_ = self.width // 8
        hex_digits = max(2, bytes_ * 2)

        return f"value=0x{self.value:0{hex_digits}x}"


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

    def describe(self) -> str:
        return f"kind={self.kind.decode()} {self.target.describe()}"
