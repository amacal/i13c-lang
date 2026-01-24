from dataclasses import dataclass

from i13c.sem.core import Identifier, Type
from i13c.sem.typing.entities.functions import FunctionId
from i13c.src import Span


@dataclass(kw_only=True, frozen=True)
class VariableId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("variable", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Variable:
    ref: Span
    type: Type
    ident: Identifier
    owner: FunctionId

    def describe(self) -> str:
        return f"Variable(ident={self.ident}, type={self.type}, owner={self.owner})"
