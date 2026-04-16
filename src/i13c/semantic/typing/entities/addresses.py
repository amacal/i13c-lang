from dataclasses import dataclass
from typing import Literal as Kind
from typing import Optional, Union

from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span

OffsetKind = Kind["forward", "backward"]
BaseRegister = Union[RegisterId, ReferenceId]


@dataclass(kw_only=True, frozen=True)
class AddressId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("address", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Offset:
    kind: OffsetKind
    value: ImmediateId

    def __str__(self) -> str:
        return f"{self.kind}/{self.value.identify(1)}"


@dataclass(kw_only=True)
class Address:
    ref: Span
    base: BaseRegister
    offset: Optional[Offset]

    def __str__(self) -> str:
        return (
            self.base.identify(1)
            if self.offset is None
            else f"{self.base.identify(1)}/{self.offset}"
        )
