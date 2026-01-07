from dataclasses import dataclass
from typing import Dict, List

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes import Block, BlockId
from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.functions import FunctionId


@dataclass(kw_only=True)
class LowLevelGraph:
    generator: Generator
    entry: BlockId

    nodes: OneToOne[BlockId, Block]
    edges: OneToMany[BlockId, BlockId]


@dataclass(kw_only=True)
class LowLevelContext:
    graph: SemanticGraph
    generator: Generator

    nodes: Dict[BlockId, Block]
    edges: Dict[BlockId, List[BlockId]]

    entry: Dict[FunctionId, BlockId]
    exit: Dict[FunctionId, BlockId]
