from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.assigns import AssignExpression, AssignId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span

AssignRejectionReason = Kind["unknown"]


@dataclass(kw_only=True)
class AssignAcceptance:
    ref: Span
    id: AssignId

    name: bytes
    type: TypeAcceptance

    destination: ValueId
    expression: AssignExpression


@dataclass(kw_only=True)
class AssignRejection:
    reason: AssignRejectionReason


@dataclass(kw_only=True)
class AssignResolution:
    accepted: List[AssignAcceptance]
    rejected: List[AssignRejection]
