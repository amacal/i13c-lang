from dataclasses import dataclass
from typing import Dict, Iterator, List

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import Instruction
from i13c.lowering.typing.stacks import StackFrame
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True)
class LowLevelGraph:
    entry: BlockId
    nodes: OneToOne[BlockId, Block]
    flows: OneToMany[BlockId, Instruction]

    forward: OneToMany[BlockId, BlockId]
    backward: OneToMany[BlockId, BlockId]

    def instructions(self) -> Iterator[Instruction]:
        for flow in self.flows.values():
            for instr in flow:
                yield instr


@dataclass(kw_only=True)
class LowLevelContext:
    graph: SemanticGraph
    generator: Generator

    nodes: Dict[BlockId, Block]
    flows: Dict[BlockId, List[Instruction]]

    forward: Dict[BlockId, List[BlockId]]
    backward: Dict[BlockId, List[BlockId]]

    entry: Dict[FunctionId, BlockId]
    exit: Dict[FunctionId, BlockId]

    stack: Dict[FunctionId, StackFrame]
    values: Dict[ExpressionId, int]

    @staticmethod
    def empty(graph: SemanticGraph) -> LowLevelContext:
        return LowLevelContext(
            graph=graph,
            generator=graph.generator,
            nodes={},
            forward={},
            backward={},
            flows={},
            entry={},
            exit={},
            stack={},
            values={},
        )
