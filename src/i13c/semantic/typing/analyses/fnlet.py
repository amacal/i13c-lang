from dataclasses import dataclass

from i13c.semantic.typing.analyses.llvm import (
    DecreaseStackPointer,
    IncreaseStackPointer,
    PopFromStackPointer,
    PushToStackPointer,
    Return,
)
from i13c.semantic.typing.analyses.statements import StatementInstruction
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span

FnletInstruction = (
    StatementInstruction
    | IncreaseStackPointer
    | PopFromStackPointer
    | PushToStackPointer
    | DecreaseStackPointer
    | Return
)


@dataclass(kw_only=True, repr=False)
class FnletBlock:
    instructions: list[FnletInstruction]


@dataclass(kw_only=True, repr=False)
class Fnlet:
    ref: Span
    target: FunctionId

    blocks: list[FnletBlock]
