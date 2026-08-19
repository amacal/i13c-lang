from dataclasses import dataclass

from i13c.semantic.typing.analyses.llvm import Call, Exchange, Move
from i13c.semantic.typing.resolutions.calls import CallAcceptance
from i13c.syntax.source import Span

CallInstruction = Call | Move | Exchange


@dataclass(kw_only=True, repr=False)
class CallLlvm:
    ref: Span
    target: CallAcceptance
    instructions: list[CallInstruction]
