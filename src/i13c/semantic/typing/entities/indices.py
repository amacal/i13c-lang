from dataclasses import dataclass

from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class IndexId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("index", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Index:
    ref: Span

    scale: int
    target: RegisterId | ReferenceId

    def __str__(self) -> str:
        return f"{self.scale}*{self.target.identify(1)}"
