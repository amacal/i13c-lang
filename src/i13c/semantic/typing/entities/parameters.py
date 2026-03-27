from dataclasses import dataclass

from i13c.semantic.core import Identifier, Type
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ParameterId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("parameter", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Parameter:
    ref: Span
    type: Type
    ident: Identifier

    def __str__(self) -> str:
        return f"{self.ident}:{self.type}"
