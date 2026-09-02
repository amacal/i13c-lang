from dataclasses import dataclass

from i13c.semantic.typing.entities.displacements import DisplacementId
from i13c.semantic.typing.entities.indices import IndexId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span

BaseRegister = RegisterId | ReferenceId


@dataclass(kw_only=True, frozen=True)
class AddressId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("address", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Address:
    ref: Span
    size: bytes | None
    base: BaseRegister | None
    indx: IndexId | None
    disp: DisplacementId | None

    def __str__(self) -> str:
        parts: list[str] = []

        if self.base is not None:
            parts.append(str(self.base))

        if self.indx is not None:
            parts.append(str(self.indx))

        if self.disp is not None:
            parts.append(str(self.disp))

        return "/".join(parts)
