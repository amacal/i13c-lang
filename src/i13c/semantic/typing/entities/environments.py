from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.identifiers.labels import LabelId
from i13c.semantic.typing.identifiers.signatures import SignatureId
from i13c.semantic.typing.identifiers.snippets import SnippetId
from i13c.syntax.source import Span

EnvironmentKind = Kind["snippet"]
EnvironmentTarget = SignatureId | LabelId


@dataclass(kw_only=True)
class Environment:
    ref: Span

    ctx: SnippetId
    kind: EnvironmentKind
    entries: list[EnvironmentTarget]

    def __str__(self) -> str:
        return f"{self.kind}:{len(self.entries)}@{self.ctx.identify(1)}"
