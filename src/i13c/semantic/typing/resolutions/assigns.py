from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.resolutions.expressions import ExpressionAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

AssignRejectionReason = Kind["unknown"]
AssignExpression = LiteralAcceptance | ExpressionAcceptance


@dataclass(kw_only=True)
class AssignAcceptance:
    ref: Span
    id: AssignId

    destination: ValueAcceptance
    expression: AssignExpression


@dataclass(kw_only=True)
class AssignRejection:
    reason: AssignRejectionReason


@dataclass(kw_only=True)
class AssignResolution:
    accepted: list[AssignAcceptance]
    rejected: list[AssignRejection]
