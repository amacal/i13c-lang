from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.ranges import RangeId
from i13c.syntax.source import Span

RangeRejectionReason = Kind["lower-greater-than-upper"]


@dataclass(kw_only=True)
class RangeRejection:
    ref: Span
    reason: RangeRejectionReason


@dataclass(kw_only=True)
class RangeAcceptance:
    ref: Span
    id: RangeId

    lower: Hex
    upper: Hex


@dataclass(kw_only=True)
class RangeResolution:
    accepted: List[RangeAcceptance]
    rejected: List[RangeRejection]
