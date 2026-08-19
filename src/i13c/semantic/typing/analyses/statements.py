from dataclasses import dataclass

from i13c.semantic.typing.analyses.llvm import Call, Exchange, Move
from i13c.semantic.typing.resolutions.statements import StatementAcceptance
from i13c.syntax.source import Span

StatementInstruction = Call | Move | Exchange


@dataclass(kw_only=True, repr=False)
class StatementLlvm:
    ref: Span
    acceptance: StatementAcceptance
    instructions: list[StatementInstruction]
