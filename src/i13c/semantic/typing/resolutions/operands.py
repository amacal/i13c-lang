from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.operand import OperandId
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

OperandKind = Kind["register", "immediate", "reference", "address"]
OperandTarget = Union[RegisterAcceptance, ImmediateAcceptance, ReferenceAcceptance, AddressAcceptance]

OperandRejectionReason = Kind["unsupported-register"]


@dataclass(kw_only=True)
class OperandRejection:
    ref: Span

    kind: OperandKind
    reason: OperandRejectionReason


@dataclass(kw_only=True)
class OperandAcceptance:
    ref: Span
    id: OperandId

    kind: OperandKind
    target: OperandTarget


@dataclass(kw_only=True)
class OperandResolution:
    accepted: List[OperandAcceptance]
    rejected: List[OperandRejection]
