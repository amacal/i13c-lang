from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from i13c.semantic.syntax import NodeId
from i13c.syntax.source import Span

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
