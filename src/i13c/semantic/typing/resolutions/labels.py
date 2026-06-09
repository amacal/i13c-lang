from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.labels import LabelId, LabelTarget
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class LabelRejection:
    ref: Span
    id: LabelId


@dataclass(kw_only=True)
class LabelAcceptance:
    ref: Span
    id: LabelId

    index: int
    name: bytes
    target: LabelTarget

    def __str__(self) -> str:
        return f"@{self.name.decode()}"


@dataclass(kw_only=True)
class LabelResolution:
    ref: Span
    id: LabelId

    accepted: List[LabelAcceptance]
    rejected: List[LabelRejection]
