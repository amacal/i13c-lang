from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.semantic.core import Identifier, Type
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.src import Span

ExpressionKind = Kind[b"literal", b"expression"]
ExpressionTarget = Union[LiteralId, ExpressionId]


@dataclass(kw_only=True, frozen=True)
class ValueId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("value", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Expression:
    kind: ExpressionKind
    target: ExpressionTarget


@dataclass(kw_only=True)
class Value:
    ref: Span
    id: ValueId
    type: Type
    ident: Identifier
    expr: Expression

    def __str__(self) -> str:
        return f"{self.ident}:{self.type},  expr={self.expr.target.identify(1)}"
