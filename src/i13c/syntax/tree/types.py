from dataclasses import dataclass
from typing import Optional, Protocol

from i13c.syntax.source import Span
from i13c.syntax.tree.core import Path
from i13c.syntax.tree.literals import Hex


class Visitor(Protocol):
    def on_type(self, type: Type, path: Path) -> None: ...
    def on_range(self, range: Range, path: Path) -> None: ...


@dataclass(kw_only=True, eq=False)
class Type:
    ref: Span
    name: bytes
    range: Optional[Range]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_type(self, path)

        with path.push(self) as node:
            if self.range is not None:
                self.range.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Range:
    ref: Span
    lower: Hex
    upper: Hex

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_range(self, path)
