from dataclasses import dataclass

from i13c.semantic.typing.entities.types import TypeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ResultId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("result", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Result:
    ref: Span
    type: TypeId
