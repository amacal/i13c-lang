from dataclasses import dataclass
from typing import Set, Union

from i13c.llvm.typing.abstracts import AbstractEntry, AbstractId
from i13c.llvm.typing.flows import BlockId, FlowEntry, FlowId
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.terminators import Terminator
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.entities.values import ValueId

BlockOrigin = Union[FunctionId, SnippetId, CallSiteId, ValueId]
BlockInstruction = Union[InstructionEntry, AbstractEntry, FlowEntry]
BlockInstructionId = Union[InstructionId, AbstractId, FlowId]


@dataclass(kw_only=True)
class InstructionPosition:
    target: BlockInstructionId
    block: BlockId
    index: int


@dataclass
class Registers:
    items: Set[int]

    @staticmethod
    def empty() -> Registers:
        return Registers(items=set())

    @staticmethod
    def instance(registers: Set[int]) -> Registers:
        return Registers(items=registers)


@dataclass(kw_only=True)
class Block:
    origin: BlockOrigin
    terminator: Terminator

    # registers: Registers
    # instructions: List[BlockInstruction]
