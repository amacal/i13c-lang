from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.addresses import AddressId
from i13c.semantic.typing.resolutions.displacements import DisplacementAcceptance
from i13c.semantic.typing.resolutions.indices import IndexAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

AddressRejectionReason = Kind[
    "invalid-register",
    "invalid-index",
    "invalid-size",
]

AddressSize = Kind[8, 16, 32, 64]
AddressBase = RegisterAcceptance | ParameterAcceptance


@dataclass(kw_only=True)
class AddressRejection:
    ref: Span
    id: AddressId

    reason: AddressRejectionReason


@dataclass(kw_only=True)
class AddressAcceptance:
    ref: Span
    id: AddressId

    size: AddressSize
    base: AddressBase | None
    indx: IndexAcceptance | None
    disp: DisplacementAcceptance | None

    def __str__(self) -> str:
        output = ""

        if self.base is not None:
            output += self.base.name.decode()

        if self.indx is not None:
            output += f" {self.indx}"

        if self.disp is not None:
            output += f" {self.disp}"

        return f"[{output}]"


@dataclass(kw_only=True)
class AddressResolution:
    ref: Span
    id: AddressId

    accepted: list[AddressAcceptance]
    rejected: list[AddressRejection]
