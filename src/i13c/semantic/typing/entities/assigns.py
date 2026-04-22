from dataclasses import dataclass
from typing import Union

from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.values import ValueId
from i13c.syntax.source import Span

AssignExpression = Union[LiteralId, ExpressionId]


@dataclass(kw_only=True, frozen=True)
class AssignId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("assign", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Assign:
    ref: Span

    destination: ValueId
    expression: AssignExpression
