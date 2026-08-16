from dataclasses import dataclass

from i13c.semantic.typing.analyses.cflows import FlowMember
from i13c.semantic.typing.analyses.dflows import FlowValue
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span

SpillNode = FlowMember
SpillValue = FlowValue


@dataclass(kw_only=True)
class SpillReg:
    slot: int
    src: bytes


@dataclass(kw_only=True)
class SpillScratch:
    slot: int
    src: bytes


SpillOp = SpillReg | SpillScratch


@dataclass(kw_only=True)
class Spill:
    ref: Span
    target: FunctionId

    entry: int
    exit: int

    nodes: list[SpillNode]
    values: list[SpillValue]

    # CFG Node -> CFG Nodes
    forward: dict[int, list[int]]
    backward: dict[int, list[int]]

    # CFG Node -> Spill Operations
    spills: dict[int, list[SpillOp]]
