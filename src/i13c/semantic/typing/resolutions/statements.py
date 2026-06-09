from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.calls import CallAcceptance
from i13c.syntax.source import Span

StatementRejectionReason = Kind["unknown"]
StatementTarget = Union[AssignAcceptance, CallAcceptance]


@dataclass(kw_only=True)
class StatementAcceptance:
    ref: Span
    id: StatementId

    target: StatementTarget


@dataclass(kw_only=True)
class StatementRejection:
    ref: Span
    id: StatementId
    reason: StatementRejectionReason


@dataclass(kw_only=True)
class StatementResolution:
    ref: Span
    id: StatementId

    accepted: List[StatementAcceptance]
    rejected: List[StatementRejection]
