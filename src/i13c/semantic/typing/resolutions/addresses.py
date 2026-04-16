from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Union

from i13c.semantic.typing.entities.addresses import AddressId, OffsetKind
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

AddressRejectionReason = Kind[
    "invalid-register",
    "invalid-offset",
]

AddressBase = Union[RegisterAcceptance, ReferenceAcceptance]


@dataclass(kw_only=True)
class AddressRejection:
    ref: Span
    reason: AddressRejectionReason


@dataclass(kw_only=True)
class OffsetAcceptance:
    kind: OffsetKind
    value: ImmediateAcceptance


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
