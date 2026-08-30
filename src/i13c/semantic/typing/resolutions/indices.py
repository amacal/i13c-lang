from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.indices import IndexId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

IndexRejectionReason = Kind[
    "invalid-register",
    "invalid-scaler",
]

@dataclass(kw_only=True)
class IndexRejection:
    ref: Span
    id: IndexId

    reason: IndexRejectionReason


@dataclass(kw_only=True)
class IndexAcceptance:
    ref: Span
    id: IndexId

    scale: Kind[1, 2, 4, 8]
    target: RegisterAcceptance | ParameterAcceptance

    def __str__(self) -> str:
        return str(self.target)


@dataclass(kw_only=True)
class IndexResolution:
    ref: Span
    id: IndexId

    accepted: list[IndexAcceptance]
    rejected: list[IndexRejection]
