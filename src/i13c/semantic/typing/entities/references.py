from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from i13c.semantic.syntax import NodeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class ReferenceId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("reference", f"{self.value:<{length}}"))


SnippetIdLike = TypeVar("SnippetIdLike")


@dataclass(kw_only=True)
class Reference:
    ref: Span
    name: bytes
    snippet: NodeId

    def get_snippet(
        self, factory: Callable[[NodeId], SnippetIdLike]
    ) -> SnippetIdLike:
        return factory(self.snippet)
