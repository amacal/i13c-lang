from dataclasses import dataclass
from typing import Union

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.syntax.source import Span

StatementTarget = Union[AssignId, CallSiteId]


@dataclass(kw_only=True, frozen=True)
class StatementId:
    value: int

    @staticmethod
    def from_context(nid: NodeId) -> StatementId:
        return StatementId(value=nid.value)

    def identify(self, length: int) -> str:
        return "#".join(("statement", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Statement:
    ref: Span
    target: StatementTarget
