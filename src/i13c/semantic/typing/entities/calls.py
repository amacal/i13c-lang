from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class CallId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("call", f"{self.value:<{length}}"))


class CallContextBound(Protocol):
    pass


CallContext = TypeVar("CallContext", bound=CallContextBound)


@dataclass(kw_only=True)
class Call:
    ref: Span
    target: CallSiteId

    fn: NodeId
    stmt: NodeId

    def get_function(self, factory: Callable[[NodeId], CallContext]) -> CallContext:
        return factory(self.fn)

    def get_statement(self, factory: Callable[[NodeId], CallContext]) -> CallContext:
        return factory(self.stmt)
