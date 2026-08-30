from dataclasses import dataclass

from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span
from i13c.semantic.syntax import NodeId

@dataclass(kw_only=True, frozen=True)
class FlagsId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("flags", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Flags:
    ref: Span
    nid: NodeId

    noreturn: bool | None
    clobbers: list[RegisterId] | None

    def __str__(self) -> str:
        return f"{self.noreturn}/clobbers={len(self.clobbers or [])}"
