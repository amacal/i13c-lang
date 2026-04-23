from dataclasses import dataclass
from typing import Callable, List
from typing import Literal as Kind
from typing import TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span

ValueRejectionReason = Kind["unknown"]
ValueContext = TypeVar("ValueContext")


@dataclass(kw_only=True)
class ValueAcceptance:
    ref: Span
    id: ValueId

    stmt: NodeId

    name: bytes
    type: TypeAcceptance

    def get_statement(self, factory: Callable[[NodeId], ValueContext]) -> ValueContext:
        return factory(self.stmt)


@dataclass(kw_only=True)
class ValueRejection:
    ref: Span
    reason: ValueRejectionReason


@dataclass(kw_only=True)
class ValueResolution:
    accepted: List[ValueAcceptance]
    rejected: List[ValueRejection]
