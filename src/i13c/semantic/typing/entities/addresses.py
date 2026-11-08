from dataclasses import dataclass

from i13c.semantic.typing.identifiers.displacements import DisplacementId
from i13c.semantic.typing.identifiers.indices import IndexId
from i13c.semantic.typing.identifiers.references import ReferenceId
from i13c.semantic.typing.identifiers.registers import RegisterId
from i13c.syntax.source import Span

BaseRegister = RegisterId | ReferenceId
Displacement = DisplacementId | ReferenceId


@dataclass(kw_only=True)
class Address:
    ref: Span
    size: bytes | None
    base: BaseRegister | None
    indx: IndexId | None
    disp: Displacement | None

    def __str__(self) -> str:
        parts: list[str] = []

        if self.base is not None:
            parts.append(str(self.base))

        if self.indx is not None:
            parts.append(str(self.indx))

        if self.disp is not None:
            parts.append(str(self.disp))

        return "/".join(parts)
