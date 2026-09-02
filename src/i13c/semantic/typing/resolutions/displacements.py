from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.displacements import (
    DisplacementDirection,
    DisplacementId,
    DisplacementOffset,
)
from i13c.syntax.source import Span

DisplacementWidth = Kind[0, 8, 32]
DisplacementRejectionReason = Kind["overflow"]


@dataclass(kw_only=True)
class DisplacementRejection:
    ref: Span
    id: DisplacementId
    reason: DisplacementRejectionReason


@dataclass(kw_only=True)
class DisplacementAcceptance:
    ref: Span
    id: DisplacementId

    width: DisplacementWidth
    offset: DisplacementOffset
    direction: DisplacementDirection

    def __str__(self) -> str:
        if self.direction == "forward":
            return f"+ 0x{self.offset.hex()}"
        else:
            return f"- 0x{self.offset.hex()}"


@dataclass(kw_only=True)
class DisplacementResolution:
    ref: Span
    id: DisplacementId

    accepted: list[DisplacementAcceptance]
    rejected: list[DisplacementRejection]
