from dataclasses import dataclass

from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

FlowValue = ParameterAcceptance | ValueAcceptance | Calling


@dataclass(kw_only=True)
class DataFlows:
    ref: Span
    target: FunctionId

    entry: int
    exit: int

    values: list[FlowValue]
    forward: dict[int, list[int]]
    backward: dict[int, list[int]]

    control: ControlFlows
    defs: dict[int, list[int]]
    uses: dict[int, list[int]]
