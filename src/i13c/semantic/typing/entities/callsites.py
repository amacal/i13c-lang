from dataclasses import dataclass
from typing import Callable, List, Protocol, TypeVar, Union

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.syntax.source import Span

CallSiteTarget = Union[LiteralId, ExpressionId]


@dataclass(kw_only=True, frozen=True)
class CallSiteId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("callsite", f"{self.value:<{length}}"))


class CallSiteContextBound(Protocol):
    pass


CallSiteContext = TypeVar("CallSiteContext", bound=CallSiteContextBound)


@dataclass(kw_only=True)
class CallSite:
    ref: Span
    ctx: NodeId

    callee: bytes
    arguments: List[CallSiteTarget]

    def get_context(
        self, factory: Callable[[NodeId], CallSiteContext]
    ) -> CallSiteContext:
        return factory(self.ctx)
