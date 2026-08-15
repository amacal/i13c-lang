from dataclasses import dataclass

from i13c.semantic.typing.analyses.dflows import FlowValue
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span

AllocationValue = FlowValue


@dataclass(kw_only=True)
class Allocation:
    ref: Span
    target: FunctionId

    values: list[AllocationValue]
    colors: dict[int, int]
    spills: dict[int, int]
