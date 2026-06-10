from dataclasses import dataclass
from typing import Dict, Set

from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Liveness:
    ref: Span
    target: FunctionId

    flow: ControlFlows
    live_in: Dict[int, Set[int]]
    live_out: Dict[int, Set[int]]
