from dataclasses import dataclass

from i13c.semantic.typing.identifiers.assigns import AssignId
from i13c.semantic.typing.identifiers.calls import CallId
from i13c.syntax.source import Span

StatementTarget = AssignId | CallId


@dataclass(kw_only=True)
class Statement:
    ref: Span
    target: StatementTarget
