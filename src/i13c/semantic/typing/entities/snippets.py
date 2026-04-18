from dataclasses import dataclass
from typing import List

from i13c.semantic.core import Identifier
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("snippet", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Snippet:
    ref: Span
    identifier: Identifier
    noreturn: bool
    clobbers: List[RegisterId]
    instructions: List[InstructionId]
