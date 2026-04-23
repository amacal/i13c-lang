from dataclasses import dataclass
from typing import Callable, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.types import TypeId
from i13c.syntax.source import Span

ValueContext = TypeVar("ValueContext")


@dataclass(kw_only=True, frozen=True)
class ValueId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("value", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Value:
    ref: Span
    stmt: NodeId

    name: bytes
    type: TypeId

    def get_statement(self, factory: Callable[[NodeId], ValueContext]) -> ValueContext:
        return factory(self.stmt)
