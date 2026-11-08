from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeVar

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.identifiers.mnemonics import MnemonicId
from i13c.semantic.typing.identifiers.operands import OperandId
from i13c.syntax.source import Span


class SnippetContextBound(Protocol):
    pass


SnippetContext = TypeVar("SnippetContext", bound=SnippetContextBound)

@dataclass(kw_only=True)
class Instruction:
    ref: Span
    snippet: NodeId

    mnemonic: MnemonicId
    operands: list[OperandId]

    def get_snippet(
        self, factory: Callable[[NodeId], SnippetContext]
    ) -> SnippetContext:
        return factory(self.snippet)
