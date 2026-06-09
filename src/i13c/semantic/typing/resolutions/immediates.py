from dataclasses import dataclass
from typing import List

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class ImmediateRejection:
    ref: Span
    id: ImmediateId


@dataclass(kw_only=True)
class ImmediateAcceptance:
    ref: Span
    id: ImmediateId
    value: Hex

    def __str__(self) -> str:
        return str(self.value)


@dataclass(kw_only=True)
class ImmediateResolution:
    ref: Span
    id: ImmediateId

    accepted: List[ImmediateAcceptance]
    rejected: List[ImmediateRejection]
