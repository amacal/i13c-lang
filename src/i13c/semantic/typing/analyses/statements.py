from dataclasses import dataclass

from i13c.semantic.typing.analyses.llvm import CALL, MOV, XCHG
from i13c.semantic.typing.resolutions.statements import StatementAcceptance
from i13c.syntax.source import Span

StatementInstruction = CALL | MOV | XCHG


@dataclass(kw_only=True, repr=False)
class StatementLlvm:
    ref: Span
    acceptance: StatementAcceptance
    instructions: list[StatementInstruction]

    def listing(self) -> list[str]:
        return [str(instruction) for instruction in self.instructions]
