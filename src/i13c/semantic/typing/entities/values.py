from dataclasses import dataclass
from typing import Optional, Union

from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.types import TypeId
from i13c.syntax.source import Span

ValueTarget = Union[LiteralId, ExpressionId]


@dataclass(kw_only=True, frozen=True)
class ValueId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("value", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Value:
    ref: Span

    name: bytes
    type: TypeId

    target: Optional[ValueTarget]
