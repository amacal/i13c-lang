from dataclasses import dataclass

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


FlowTarget = StatementId
FlowMember = FlowEntry | FlowExit | FlowNode

@dataclass(kw_only=True)
class ControlFlows:
    ref: Span

    entry: int
    exit: int

    target: FunctionId
    nodes: list[FlowMember]

    # CFG Node -> CFG Nodes
    forward: dict[int, list[int]]
    backward: dict[int, list[int]]
