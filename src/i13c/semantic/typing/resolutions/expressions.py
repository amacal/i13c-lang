from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.semantic.typing.resolutions.usages import UsageAcceptance
from i13c.syntax.source import Span

ExpressionRejectionReason = Kind["unknown"]
ExpressionNode = LiteralAcceptance | UsageAcceptance | CallSiteId


@dataclass(kw_only=True)
class ExpressionAcceptance:
    ref: Span
    id: ExpressionId
    nodes: list[ExpressionNode]

    def get_node(self) -> ExpressionNode:
        assert len(self.nodes) == 1
        return self.nodes[0]


    def get_type(self) -> LiteralAcceptance | TypeAcceptance | CallSiteId:
        assert self.nodes
        node = self.nodes[0]

        if isinstance(node, LiteralAcceptance):
            return node

        if isinstance(node, UsageAcceptance):
            return node.target.type

        return node


@dataclass(kw_only=True)
class ExpressionRejection:
    ref: Span
    id: ExpressionId
    reason: ExpressionRejectionReason


@dataclass(kw_only=True)
class ExpressionResolution:
    accepted: list[ExpressionAcceptance]
    rejected: list[ExpressionRejection]
