from dataclasses import dataclass

from i13c.semantic.typing.analyses.callings import Calling, CallingClobber
from i13c.semantic.typing.analyses.cflows import FlowMember
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

FlowValue = (
    ParameterAcceptance | ValueAcceptance | LiteralAcceptance | Calling | CallingClobber
)


@dataclass(kw_only=True)
class DataFlows:
    ref: Span
    target: FunctionId

    nodes: list[FlowMember]
    values: list[FlowValue]

    # DFG Node -> DFG Nodes
    forward: dict[int, list[int]]
    backward: dict[int, list[int]]

    # CFG Node -> DFG Values
    defs: dict[int, list[int]]
    uses: dict[int, list[int]]

    # CFG Node -> DFG Values
    clobbers: dict[int, list[int]]
