from dataclasses import dataclass

from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ReferenceId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("reference", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Reference:
    ref: Span
    name: bytes
    ctx: SnippetId

    def __str__(self) -> str:
        return f"{self.name.decode()}"
