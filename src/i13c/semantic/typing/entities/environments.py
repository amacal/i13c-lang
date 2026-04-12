from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.syntax.source import Span

EnvironmentKind = Kind["snippet"]
EnvironmentTarget = Union[SignatureId, LabelId]


@dataclass(kw_only=True, frozen=True)
class EnvironmentId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("environment", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Environment:
    ref: Span

    ctx: SnippetId
    kind: EnvironmentKind
    entries: List[EnvironmentTarget]

    def __str__(self) -> str:
        return f"{self.kind}:{len(self.entries)}@{self.ctx.identify(1)}"
