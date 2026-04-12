from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span

OperandKind = Kind["register", "immediate", "reference"]
OperandTarget = Union[RegisterId, ImmediateId, ReferenceId]


@dataclass(kw_only=True, frozen=True)
class OperandId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("operand", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Operand:
    ref: Span

    kind: OperandKind
    target: OperandTarget

    def __str__(self) -> str:
        return self.target.identify(1)
