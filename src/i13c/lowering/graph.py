from dataclasses import dataclass
from typing import Iterator, Optional

from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.blocks import Block, BlockInstruction, BlockOrigin, Registers
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import Instruction
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True)
class FunctionsNode:
    entries: OneToOne[FunctionId, BlockId]
    exits: OneToOne[FunctionId, BlockId]


@dataclass(kw_only=True)
class RegistersNode:
    inputs: OneToOne[BlockId, Registers]
    outputs: OneToOne[BlockId, Registers]
    clobbers: OneToOne[BlockId, Registers]


@dataclass(kw_only=True)
class LowLevelGraph:
    entry: BlockId
    nodes: OneToOne[BlockId, Block]

    flows: OneToMany[BlockId, BlockInstruction]
    instructions: OneToMany[BlockId, Instruction]

    forward: OneToMany[BlockId, BlockId]
    backward: OneToMany[BlockId, BlockId]

    functions: FunctionsNode
    registers: RegistersNode

    def flows_all(self) -> Iterator[BlockInstruction]:
        for _, flow in self.flows.items():
            for instr in flow:
                yield instr

    def instructions_all(self) -> Iterator[Instruction]:
        for _, batch in self.instructions.items():
            for instr in batch:
                yield instr

    def instructions_of(self, origin: BlockOrigin) -> Iterator[str]:
        for bid, batch in self.instructions.items():
            if self.nodes.get(bid).origin == origin:
                for instr in batch:
                    yield instr.native()

    def find_block_by_origin(self, origin: BlockOrigin) -> Optional[BlockId]:
        for bid, block in self.nodes.items():
            if block.origin == origin:
                return bid

        return None
