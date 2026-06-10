from dataclasses import dataclass
from typing import Dict, List, Union

from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.cflows import FlowMember
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

FlowValue = Union[
    ParameterAcceptance,
    ValueAcceptance,
    Calling,
]


@dataclass(kw_only=True)
class DataFlows:
    ref: Span
    target: FunctionId

    entry: int
    exit: int

    values: List[FlowValue]
    forward: Dict[int, List[int]]
    backward: Dict[int, List[int]]

    nodes: List[FlowMember]
    defs: Dict[int, List[int]]
    uses: Dict[int, List[int]]
