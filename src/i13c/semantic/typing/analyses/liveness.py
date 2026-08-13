from dataclasses import dataclass

from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Liveness:
    ref: Span
    target: FunctionId

    flow: ControlFlows
    live_in: dict[int, set[int]]
    live_out: dict[int, set[int]]
