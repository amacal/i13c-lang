from dataclasses import dataclass
from typing import Dict, Iterator, List

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.ir import Block, BlockId, InstructionFlow
from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.functions import FunctionId


@dataclass(kw_only=True)
class LowLevelGraph:
    generator: Generator
    entry: BlockId

    nodes: OneToOne[BlockId, Block]
    edges: OneToMany[BlockId, BlockId]
    flows: OneToMany[BlockId, InstructionFlow]

    def instructions(self) -> Iterator[InstructionFlow]:
        for flow in self.flows.values():
            for instr in flow:
                yield instr


@dataclass(kw_only=True)
class LowLevelContext:
    graph: SemanticGraph
    generator: Generator

    nodes: Dict[BlockId, Block]
    edges: Dict[BlockId, List[BlockId]]
    flows: Dict[BlockId, List[InstructionFlow]]

    entry: Dict[FunctionId, BlockId]
    exit: Dict[FunctionId, BlockId]
