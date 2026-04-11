from dataclasses import dataclass
from typing import List

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class ImmediateRejection:
    ref: Span


@dataclass(kw_only=True)
class ImmediateAcceptance:
    ref: Span
    id: ImmediateId

    value: Hex


@dataclass(kw_only=True)
class ImmediateResolution:
    accepted: List[ImmediateAcceptance]
    rejected: List[ImmediateRejection]
