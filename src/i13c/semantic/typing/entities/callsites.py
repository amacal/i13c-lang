from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.syntax.source import Span


class CallSiteContextBound(Protocol):
    pass


CallSiteContext = TypeVar("CallSiteContext", bound=CallSiteContextBound)


@dataclass(kw_only=True)
class CallSite:
    ref: Span

    function: NodeId
    statement: NodeId

    callee: bytes
    arguments: list[ExpressionId]

    def get_function(
        self, factory: Callable[[NodeId], CallSiteContext]
    ) -> CallSiteContext:
        return factory(self.function)

    def get_statement(
        self, factory: Callable[[NodeId], CallSiteContext]
    ) -> CallSiteContext:
        return factory(self.statement)
