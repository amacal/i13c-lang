from dataclasses import dataclass

from i13c.semantic.typing.analyses.llvm import Move
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.syntax.source import Span

AssignInstruction = Move


@dataclass(kw_only=True, repr=False)
class AssignLlvm:
    ref: Span
    target: AssignAcceptance
    instructions: list[AssignInstruction]
