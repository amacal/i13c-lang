from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.expressions import ExpressionAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

AssignRejectionReason = Kind["type-mismatch"]


@dataclass(kw_only=True)
class AssignAcceptance:
    ref: Span
    id: AssignId

    fn: FunctionId
    stmt: StatementId

    destination: ValueAcceptance
    expression: ExpressionAcceptance


@dataclass(kw_only=True)
class AssignRejection:
    ref: Span
    id: AssignId
    reason: AssignRejectionReason


@dataclass(kw_only=True)
class AssignResolution:
    accepted: list[AssignAcceptance]
    rejected: list[AssignRejection]
