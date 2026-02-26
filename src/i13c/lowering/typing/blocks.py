from dataclasses import dataclass
from typing import Set, Union

from i13c.lowering.typing.abstracts import AbstractEntry, AbstractId
from i13c.lowering.typing.flows import BlockId, FlowEntry, FlowId
from i13c.lowering.typing.instructions import InstructionEntry, InstructionId
from i13c.lowering.typing.terminators import Terminator
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId

BlockOrigin = Union[FunctionId, SnippetId, CallSiteId]
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
