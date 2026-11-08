from dataclasses import dataclass

from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.identifiers.literals import LiteralId
from i13c.semantic.typing.identifiers.usages import UsageId
from i13c.syntax.source import Span

ExpressionNode = LiteralId | UsageId | CallSiteId


@dataclass(kw_only=True)
class Expression:
    ref: Span
    nodes: list[ExpressionNode]
