from dataclasses import dataclass
from typing import Iterator, Optional

from i13c.core.mapping import OneToMany, OneToOne
from i13c.llvm.typing.abstracts import AbstractEntry
from i13c.llvm.typing.blocks import (
    Block,
    BlockInstruction,
    BlockInstructionId,
    BlockOrigin,
    InstructionPosition,
    Registers,
)
from i13c.llvm.typing.flows import BlockId, FlowId
from i13c.llvm.typing.instructions import Instruction, InstructionEntry
from i13c.llvm.typing.intervals import IntervalPressure, RegisterInterval
from i13c.llvm.typing.registers import VirtualRegister
from i13c.llvm.typing.stacks import StackFrame
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.indices.variables import VariableId


@dataclass(kw_only=True)
class FunctionsNode:
    entries: OneToOne[FunctionId, BlockId]
    exits: OneToOne[FunctionId, BlockId]
    blocks: OneToMany[FunctionId, BlockId]
    stacks: OneToOne[FunctionId, StackFrame]
    intervals: OneToMany[FunctionId, RegisterInterval]
    pressures: OneToMany[FunctionId, IntervalPressure]
    instructions: OneToMany[FunctionId, InstructionPosition]


@dataclass(kw_only=True)
class InstructionRegistersNode:
    used: OneToOne[BlockInstructionId, Registers]
    inputs: OneToOne[BlockInstructionId, Registers]
    outputs: OneToOne[BlockInstructionId, Registers]
    clobbers: OneToOne[BlockInstructionId, Registers]
    generated: OneToOne[BlockInstructionId, Registers]


@dataclass(kw_only=True)
class BlockRegistersNode:
    used: OneToOne[BlockId, Registers]
    inputs: OneToOne[BlockId, Registers]
    outputs: OneToOne[BlockId, Registers]
    clobbers: OneToOne[BlockId, Registers]
    generated: OneToOne[BlockId, Registers]


@dataclass(kw_only=True)
class PatchesNode:
    clobbers: OneToMany[FlowId, InstructionEntry]
    bindings: OneToMany[FlowId, InstructionEntry]
    snapshots: OneToMany[FlowId, InstructionEntry]
    callsites: OneToMany[FlowId, InstructionEntry]
    stackframes: OneToMany[FlowId, AbstractEntry]


@dataclass(kw_only=True)
class LowLevelGraph:
    entry: BlockId
    nodes: OneToOne[BlockId, Block]

    flows: OneToMany[BlockId, BlockInstruction]
    instructions: OneToMany[BlockId, Instruction]

    forward: OneToMany[BlockId, BlockId]
    backward: OneToMany[BlockId, BlockId]
    registers: OneToOne[VariableId, VirtualRegister]

    functions: FunctionsNode
    patches: PatchesNode

    iregs: InstructionRegistersNode
    bregs: BlockRegistersNode

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
