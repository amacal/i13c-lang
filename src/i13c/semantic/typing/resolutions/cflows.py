from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.cflows import FlowEntry, FlowExit, FlowTarget
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.values import ValueId
from i13c.syntax.source import Span

ControlFlowMember = Union[FlowEntry, FlowExit, FlowTarget]
ControlFlowTarget = Union[ParameterId, ValueId]

ControlFlowRejectionReason = Kind["unknown",]
ControlFlowEntry = Dict[bytes, ControlFlowTarget]
ControlFlowEnvironment = Dict[ControlFlowMember, ControlFlowEntry]


@dataclass(kw_only=True)
class ControlFlowRejection:
    ref: Span
    reason: ControlFlowRejectionReason


@dataclass(kw_only=True)
class ControlFlowAcceptance:
    ref: Span
    id: FunctionId

    entry: FlowEntry
    exit: FlowExit

    environments: ControlFlowEnvironment


@dataclass(kw_only=True)
class ControlFlowResolution:
    accepted: List[ControlFlowAcceptance]
    rejected: List[ControlFlowRejection]
