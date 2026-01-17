from dataclasses import dataclass
from typing import Dict, Iterator, List

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import Instruction
from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.functions import FunctionId


@dataclass(kw_only=True)
class LowLevelGraph:
    generator: Generator
    entry: BlockId

    nodes: OneToOne[BlockId, Block]
    edges: OneToMany[BlockId, BlockId]
    flows: OneToMany[BlockId, Instruction]

    def instructions(self) -> Iterator[Instruction]:
        for flow in self.flows.values():
            for instr in flow:
                yield instr


@dataclass(kw_only=True)
class LowLevelContext:
    graph: SemanticGraph
    generator: Generator

    nodes: Dict[BlockId, Block]
    edges: Dict[BlockId, List[BlockId]]
    flows: Dict[BlockId, List[Instruction]]

    entry: Dict[FunctionId, BlockId]
    exit: Dict[FunctionId, BlockId]

    @staticmethod
    def empty(graph: SemanticGraph) -> LowLevelContext:
        return LowLevelContext(
            graph=graph,
            generator=graph.generator,
            nodes={},
            edges={},
            flows={},
            entry={},
            exit={},
        )
