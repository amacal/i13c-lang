from dataclasses import dataclass
from typing import List

from i13c.sem.core import Identifier, Type
from i13c.sem.typing.entities.instructions import Binding, InstructionId
from i13c.sem.typing.entities.operands import Register
from i13c.src import Span


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("snippet", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Slot:
    name: Identifier
    type: Type
    bind: Binding

    def signature(self) -> str:
        return f"{self.name}@{self.bind}:{self.type}"


@dataclass(kw_only=True)
class Snippet:
    ref: Span
    identifier: Identifier
    noreturn: bool
    slots: List[Slot]
    clobbers: List[Register]
    instructions: List[InstructionId]

    def signature(self) -> str:
        slots = ", ".join([slot.signature() for slot in self.slots])
        return f"{self.identifier.name.decode()}/{len(self.slots)} ({slots})"

    def describe(self) -> str:
        return f"name={self.identifier.name.decode()}/{len(self.slots)}"
