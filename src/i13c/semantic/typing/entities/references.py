from dataclasses import dataclass
from typing import Protocol

from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ReferenceId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("reference", f"{self.value:<{length}}"))


class ReferenceContext(Protocol):
    @property
    def value(self) -> int: ...

    def identify(self, length: int) -> str: ...


@dataclass(kw_only=True)
class Reference:
    ref: Span
    name: bytes
    ctx: ReferenceContext

    def __str__(self) -> str:
        return f"{self.name.decode()}@{self.ctx.identify(1)}"
