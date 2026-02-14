from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Tuple

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.blocks import Block, BlockOrigin
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

    def instructions(
        self, origin: Optional[BlockOrigin] = None
    ) -> Iterator[Instruction]:
        for bid, flow in self.flows.items():
            if origin is None or self.nodes.get(bid).origin == origin:
                for instr in flow:
                    yield instr

    def instructions_of(self, origin: BlockOrigin) -> Iterator[Tuple[str, ...]]:
        for bid, flow in self.flows.items():
            if self.nodes.get(bid).origin == origin:
                for instr in flow:
                    yield instr.raw()

    def find_block_by_origin(self, origin: BlockOrigin) -> Optional[BlockId]:
        for bid, block in self.nodes.items():
            if block.origin == origin:
                return bid

        return None


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
