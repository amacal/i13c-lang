from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.semantic.core import Identifier, Type
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.src import Span

VariableKind = Kind[b"parameter"]
VariableSource = Union[ParameterId]


@dataclass(kw_only=True, frozen=True)
class VariableId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("variable", f"{self.value:<{length}}"))

    def describe(self) -> str:
        return f"var#{self.value}"


@dataclass(kw_only=True)
class Variable:
    ref: Span
    kind: VariableKind
    source: VariableSource

    type: Type
    ident: Identifier

    def describe(self) -> str:
        return f"source={self.source.identify(2)}, type={self.type}, ident={self.ident}"
