from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional

from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.resolutions.ranges import RangeAcceptance
from i13c.syntax.source import Span

TypeRejectionReason = Kind[
    "unknown-type",
    "inconsistent-widths",
]

TypeWidth = Kind[8, 16, 32, 64]


@dataclass(kw_only=True)
class TypeRejection:
    ref: Span
    reason: TypeRejectionReason


@dataclass(kw_only=True)
class TypeAcceptance:
    ref: Span
    id: TypeId

    name: bytes
    width: TypeWidth
    range: Optional[RangeAcceptance]


@dataclass(kw_only=True)
class TypeResolution:
    accepted: List[TypeAcceptance]
    rejected: List[TypeRejection]
