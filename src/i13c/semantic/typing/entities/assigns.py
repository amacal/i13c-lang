from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.identifiers.expressions import ExpressionId
from i13c.semantic.typing.identifiers.values import ValueId
from i13c.syntax.source import Span


class AssignContextBound(Protocol):
    pass


AssignContext = TypeVar("AssignContext", bound=AssignContextBound)


@dataclass(kw_only=True)
class Assign:
    ref: Span
    fn: NodeId
    stmt: NodeId

    destination: ValueId
    expression: ExpressionId

    def get_function(
        self, factory: Callable[[NodeId], AssignContext]
    ) -> AssignContext:
        return factory(self.fn)

    def get_statement(
        self, factory: Callable[[NodeId], AssignContext]
    ) -> AssignContext:
        return factory(self.stmt)
