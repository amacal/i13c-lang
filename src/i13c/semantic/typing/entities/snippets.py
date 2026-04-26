from dataclasses import dataclass
from typing import List, Optional, Union

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.syntax.source import Span

InstructionOrLabel = Union[
    InstructionId,
    LabelId,
]


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int

    @staticmethod
    def from_context(nid: NodeId) -> SnippetId:
        return SnippetId(value=nid.value)

    def identify(self, length: int) -> str:
        return "#".join(("snippet", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Snippet:
    ref: Span
    signature: SignatureId

    flags: Optional[FlagsId]
    body: List[InstructionOrLabel]
