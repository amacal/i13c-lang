from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.labels import LabelId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class LabelRejection:
    ref: Span


@dataclass(kw_only=True)
class LabelAcceptance:
    ref: Span
    id: LabelId

    name: bytes


@dataclass(kw_only=True)
class LabelResolution:
    accepted: List[LabelAcceptance]
    rejected: List[LabelRejection]
