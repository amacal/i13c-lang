from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId

CallableKind = Kind[b"snippet", b"function"]
CallableTarget = Union[SnippetId, FunctionId]


@dataclass(kw_only=True)
class Callable:
    kind: CallableKind
    target: CallableTarget

    def describe(self) -> str:
        return f"kind={self.kind.decode()} target={self.target.identify(2)}"
