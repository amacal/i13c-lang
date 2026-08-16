from dataclasses import dataclass

from i13c.semantic.typing.analyses.cflows import FlowMember
from i13c.semantic.typing.analyses.dflows import FlowValue
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


@dataclass(kw_only=True, repr=False)
class Liveness:
    ref: Span
    target: FunctionId

    nodes: list[FlowMember]
    values: list[FlowValue]

    # CFG Node -> DFG Values
    live_in: dict[int, set[int]]
    live_out: dict[int, set[int]]

    # CFG Node -> DFG Nodes
    clobbers: dict[int, set[int]]
