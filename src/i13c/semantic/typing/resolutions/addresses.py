from dataclasses import dataclass
from typing import Literal as Kind

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
AddressBase = RegisterAcceptance | ParameterAcceptance


@dataclass(kw_only=True)
class AddressRejection:
    ref: Span
    id: AddressId

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
    offset: OffsetAcceptance | None

    def __str__(self) -> str:
        output = self.base.name.decode()

        if self.offset is not None:
            if self.offset.kind == "forward":
                output += f" + {self.offset.value.value}"
            else:
                output += f" - {self.offset.value.value}"

        return f"[{output}]"


@dataclass(kw_only=True)
class AddressResolution:
    ref: Span
    id: AddressId

    accepted: list[AddressAcceptance]
    rejected: list[AddressRejection]
