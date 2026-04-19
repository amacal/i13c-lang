from dataclasses import dataclass
from typing import List, Optional

from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("snippet", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Snippet:
    ref: Span
    signature: SignatureId
    flags: Optional[FlagsId]
    instructions: List[InstructionId]
