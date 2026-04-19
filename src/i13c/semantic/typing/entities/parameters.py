from dataclasses import dataclass

from i13c.semantic.typing.entities.types import TypeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ParameterId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("parameter", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Parameter:
    ref: Span
    name: bytes
    type: TypeId

    def __str__(self) -> str:
        return f"{self.name.decode()}, {self.type.identify(1)}"
