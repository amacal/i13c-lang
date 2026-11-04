from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from i13c.semantic.syntax import NodeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class UsageId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("usage", f"{self.value:<{length}}"))


UsageContext = TypeVar("UsageContext")


@dataclass(kw_only=True)
class Usage:
    ref: Span
    name: bytes

    function: NodeId
    statement: NodeId

    def get_function(
        self, factory: Callable[[NodeId], UsageContext]
    ) -> UsageContext:
        return factory(self.function)

    def get_statement(
        self, factory: Callable[[NodeId], UsageContext]
    ) -> UsageContext:
        return factory(self.statement)
