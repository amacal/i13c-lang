from dataclasses import dataclass

from i13c.semantic.typing.identifiers.references import ReferenceId
from i13c.semantic.typing.identifiers.registers import RegisterId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Index:
    ref: Span

    scale: int
    target: RegisterId | ReferenceId

    def __str__(self) -> str:
        return f"{self.scale}*{self.target.identify(1)}"
