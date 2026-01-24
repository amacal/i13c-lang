from dataclasses import dataclass

from i13c.sem.core import Identifier
from i13c.src import Span


@dataclass(kw_only=True, frozen=True)
class UsageId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("usage", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Usage:
    ref: Span
    ident: Identifier

    def describe(self) -> str:
        return f"ident={self.ident}"
