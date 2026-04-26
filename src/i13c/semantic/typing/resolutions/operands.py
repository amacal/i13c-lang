from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.operands import OperandId
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

OperandRejectionReason = Kind["unsupported-register"]
OperandKind = Kind["register", "immediate", "parameter", "relocation", "address"]

OperandTarget = Union[
    RegisterAcceptance,
    ImmediateAcceptance,
    ParameterAcceptance,
    LabelAcceptance,
    AddressAcceptance,
]

OperandSymbol = Kind[
    "reg8",
    "reg16",
    "reg32",
    "reg64",
    "imm8",
    "imm16",
    "imm32",
    "imm64",
    "addr",
    "rel",
]


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
    symbol: OperandSymbol


@dataclass(kw_only=True)
class OperandResolution:
    accepted: List[OperandAcceptance]
    rejected: List[OperandRejection]
