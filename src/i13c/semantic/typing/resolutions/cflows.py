from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.cflows import (
    ControlFlows,
    FlowEntry,
    FlowExit,
    FlowTarget,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

ControlFlowMember = Union[FlowEntry, FlowExit, FlowTarget]
ControlFlowTarget = Union[ParameterAcceptance, ValueAcceptance]

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
    source: ControlFlows
    function: FunctionId
    signature: SignatureId

    entry: FlowEntry
    exit: FlowExit
    environments: ControlFlowEnvironment


@dataclass(kw_only=True)
class ControlFlowResolution:
    accepted: List[ControlFlowAcceptance]
    rejected: List[ControlFlowRejection]
