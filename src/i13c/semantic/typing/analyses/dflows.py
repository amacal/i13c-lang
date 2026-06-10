from dataclasses import dataclass
from typing import Dict, List, Union

from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

FlowMember = Union[
    ParameterAcceptance,
    LiteralId,
    ValueAcceptance,
    Calling,
]


@dataclass(kw_only=True)
class DataFlows:
    ref: Span
    target: FunctionId

    nodes: List[FlowMember]
    forward: Dict[int, List[int]]
    backward: Dict[int, List[int]]
