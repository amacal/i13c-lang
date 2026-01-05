from dataclasses import dataclass

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes import Block, BlockId


@dataclass(kw_only=True)
class LowLevelGraph:
    generator: Generator
    entry: BlockId

    nodes: OneToOne[BlockId, Block]
    edges: OneToMany[BlockId, BlockId]
