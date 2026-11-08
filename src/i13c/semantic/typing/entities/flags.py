from dataclasses import dataclass

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.identifiers.registers import RegisterId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Flags:
    ref: Span
    nid: NodeId

    noreturn: bool | None
    clobbers: list[RegisterId] | None

    def __str__(self) -> str:
        return f"{self.noreturn}/clobbers={len(self.clobbers or [])}"
