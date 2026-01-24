from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.sem.typing.entities.parameters import ParameterId

VariableKind = Kind[b"parameter"]
VariableSource = Union[ParameterId]


@dataclass(kw_only=True, frozen=True)
class VariableId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("variable", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Variable:
    kind: VariableKind
    source: VariableSource
