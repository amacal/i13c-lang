from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.identifiers.addresses import AddressId
from i13c.semantic.typing.identifiers.immediates import ImmediateId
from i13c.semantic.typing.identifiers.references import ReferenceId
from i13c.semantic.typing.identifiers.registers import RegisterId
from i13c.syntax.source import Span

OperandKind = Kind["register", "immediate", "reference", "address"]
OperandTarget = RegisterId | ImmediateId | ReferenceId | AddressId


@dataclass(kw_only=True)
class Operand:
    ref: Span

    kind: OperandKind
    target: OperandTarget

    def __str__(self) -> str:
        return self.target.identify(1)
