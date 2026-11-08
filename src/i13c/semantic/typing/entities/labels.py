from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.identifiers.instructions import InstructionId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class EndOfSnippet:
    def identify(self, length: int) -> str:
        return "end-of-snippet"


LabelTarget = InstructionId | EndOfSnippet


SnippetIdLike = TypeVar("SnippetIdLike")


@dataclass(kw_only=True)
class Label:
    ref: Span
    name: bytes
    index: int

    snippet: NodeId
    target: LabelTarget

    def get_snippet(
        self, factory: Callable[[NodeId], SnippetIdLike]
    ) -> SnippetIdLike:
        return factory(self.snippet)
