from dataclasses import dataclass

from i13c.semantic.typing.entities.results import ResultId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class ResultRejection:
    ref: Span
    id: ResultId


@dataclass(kw_only=True, repr=False)
class ResultAcceptance:
    ref: Span

    id: ResultId
    type: TypeAcceptance

    def __str__(self) -> str:
        return f"{self.id}:{self.type}"


@dataclass(kw_only=True)
class ResultResolution:
    ref: Span
    id: ResultId

    accepted: list[ResultAcceptance]
    rejected: list[ResultRejection]
