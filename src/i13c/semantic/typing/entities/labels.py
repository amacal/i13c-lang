from dataclasses import dataclass
from typing import Callable, Protocol, TypeVar, Union

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class EndOfSnippet:
    pass


LabelTarget = Union[
    InstructionId,
    EndOfSnippet,
]


@dataclass(kw_only=True, frozen=True)
class LabelId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("label", f"{self.value:<{length}}"))


class SnippetContextBound(Protocol):
    pass


SnippetContext = TypeVar("SnippetContext", bound=SnippetContextBound)


@dataclass(kw_only=True)
class Label:
    ref: Span
    name: bytes

    snippet: NodeId
    target: LabelTarget

    def get_snippet(
        self, factory: Callable[[NodeId], SnippetContext]
    ) -> SnippetContext:
        return factory(self.snippet)
