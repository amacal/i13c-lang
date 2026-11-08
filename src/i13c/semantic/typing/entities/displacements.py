from dataclasses import dataclass
from typing import Literal as Kind

from i13c.syntax.source import Span

DisplacementOffset = bytes
DisplacementDirection = Kind["forward", "backward"]


@dataclass(kw_only=True)
class Displacement:
    ref: Span

    offset: DisplacementOffset
    direction: DisplacementDirection

    def __str__(self) -> str:
        if self.direction == "forward":
            return f"+ 0x{self.offset.hex()}"
        else:
            return f"- 0x{self.offset.hex()}"
