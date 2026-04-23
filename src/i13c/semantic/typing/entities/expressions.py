from dataclasses import dataclass
from typing import Callable, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ExpressionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("expression", f"{self.value:<{length}}"))


ExpressionContext = TypeVar("ExpressionContext")


@dataclass(kw_only=True)
class Expression:
    ref: Span
    name: bytes

    function: NodeId
    statement: NodeId

    def get_function(
        self, factory: Callable[[NodeId], ExpressionContext]
    ) -> ExpressionContext:
        return factory(self.function)

    def get_statement(
        self, factory: Callable[[NodeId], ExpressionContext]
    ) -> ExpressionContext:
        return factory(self.statement)
