from dataclasses import dataclass

from i13c.semantic.typing.analyses.dflows import FlowValue
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Allocation:
    ref: Span
    target: FunctionId

    values: list[FlowValue]
    colors: dict[int, int]
