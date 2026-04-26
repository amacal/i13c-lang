from dataclasses import dataclass
from typing import Callable, List, Protocol, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.semantic.typing.entities.operands import OperandId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


class SnippetContextBound(Protocol):
    pass


SnippetContext = TypeVar("SnippetContext", bound=SnippetContextBound)

@dataclass(kw_only=True)
class Instruction:
    ref: Span
    snippet: NodeId

    mnemonic: MnemonicId
    operands: List[OperandId]

    def get_snippet(
        self, factory: Callable[[NodeId], SnippetContext]
    ) -> SnippetContext:
        return factory(self.snippet)
