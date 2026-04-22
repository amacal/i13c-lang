from dataclasses import dataclass
from typing import Dict, List, Union

from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class FlowEntry:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("entry", f"{self.value:<{length}}"))

@dataclass(kw_only=True, frozen=True)
class FlowExit:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("exit", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class FlowNode:
    target: FlowTarget

    def identify(self, length: int) -> str:
        return self.target.identify(length)


FlowTarget = Union[StatementId]
FlowMember = Union[FlowEntry, FlowExit, FlowNode]

@dataclass(kw_only=True)
class ControlFlows:
    ref: Span

    target: FunctionId
    nodes: List[FlowMember]

    forward: Dict[int, List[int]]
    backward: Dict[int, List[int]]
