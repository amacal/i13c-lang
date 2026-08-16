from dataclasses import dataclass

from i13c.semantic.typing.analyses.dflows import FlowValue
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span

AllocationValue = FlowValue


@dataclass(kw_only=True, repr=False)
class Allocation:
    ref: Span
    target: FunctionId

    values: list[AllocationValue]
    scratch: int

    # DGF Node -> Register
    colors: dict[int, int]

    # DGF Node -> Slot
    spills: dict[int, int]
