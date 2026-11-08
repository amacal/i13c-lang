from dataclasses import dataclass

from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.usages import UsageId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.syntax.source import Span

ExpressionNode = LiteralId | UsageId | CallSiteId


@dataclass(kw_only=True, frozen=True)
class ExpressionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("expression", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Expression:
    ref: Span
    nodes: list[ExpressionNode]
