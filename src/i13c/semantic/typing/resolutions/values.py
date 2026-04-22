from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span

ValueRejectionReason = Kind["unknown"]


@dataclass(kw_only=True)
class ValueAcceptance:
    ref: Span
    id: ValueId

    name: bytes
    type: TypeAcceptance


@dataclass(kw_only=True)
class ValueRejection:
    ref: Span
    reason: ValueRejectionReason


@dataclass(kw_only=True)
class ValueResolution:
    accepted: List[ValueAcceptance]
    rejected: List[ValueRejection]
