from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.core import Identifier
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.src import Span

ArgumentKind = Kind[b"literal", b"expression"]
ArgumentTarget = Union[LiteralId, ExpressionId]


@dataclass(kw_only=True, frozen=True)
class CallSiteId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("callsite", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Argument:
    kind: ArgumentKind
    target: ArgumentTarget


@dataclass(kw_only=True)
class CallSite:
    ref: Span
    id: CallSiteId
    callee: Identifier
    arguments: List[Argument]

    def describe(self) -> str:
        return f"name={self.callee.name.decode()}/{len(self.arguments)}"
