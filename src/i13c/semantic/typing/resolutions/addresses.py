from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Union

from i13c.semantic.typing.entities.addresses import AddressId, OffsetKind
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

AddressRejectionReason = Kind[
    "invalid-register",
    "invalid-offset",
]

OffsetWidth = Kind[8, 16, 32]
AddressBase = Union[RegisterAcceptance, ParameterAcceptance]


@dataclass(kw_only=True)
class AddressRejection:
    ref: Span
    reason: AddressRejectionReason


@dataclass(kw_only=True)
class OffsetAcceptance:
    kind: OffsetKind
    width: OffsetWidth
    value: ImmediateAcceptance

    @property
    def data(self) -> bytes:
        return self.value.value.data


@dataclass(kw_only=True)
class AddressAcceptance:
    ref: Span
    id: AddressId

    base: AddressBase
    offset: Optional[OffsetAcceptance]


@dataclass(kw_only=True)
class AddressResolution:
    accepted: List[AddressAcceptance]
    rejected: List[AddressRejection]
