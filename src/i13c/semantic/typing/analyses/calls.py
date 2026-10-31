from dataclasses import dataclass

from i13c.semantic.typing.analyses.llvm import CALL
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.calls import CallAcceptance
from i13c.syntax.source import Span

CallInstruction = CALL
CallTarget = CallAcceptance | AssignAcceptance


@dataclass(kw_only=True, repr=False)
class CallLlvm:
    ref: Span
    target: CallTarget
    instructions: list[CallInstruction]

    def listing(self) -> list[str]:
        return [str(instruction) for instruction in self.instructions]
