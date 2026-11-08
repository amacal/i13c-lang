from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.identifiers.types import TypeId
from i13c.syntax.source import Span

ValueContext = TypeVar("ValueContext")


@dataclass(kw_only=True)
class Value:
    ref: Span
    stmt: NodeId

    name: bytes
    type: TypeId

    def get_statement(self, factory: Callable[[NodeId], ValueContext]) -> ValueContext:
        return factory(self.stmt)
