from dataclasses import dataclass

from i13c.llvm.typing.abstracts import AbstractEntry, AbstractId
from i13c.llvm.typing.flows import BlockId, FlowEntry, FlowId
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.terminators import Terminator
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.entities.values import ValueId

BlockOrigin = FunctionId | SnippetId | CallSiteId | ValueId
BlockInstruction = InstructionEntry | AbstractEntry | FlowEntry
BlockInstructionId = InstructionId | AbstractId | FlowId


@dataclass(kw_only=True)
class InstructionPosition:
    target: BlockInstructionId
    block: BlockId
    index: int


@dataclass
class Registers:
    items: set[int]

    @staticmethod
    def empty() -> Registers:
        return Registers(items=set())

    @staticmethod
    def instance(registers: set[int]) -> Registers:
        return Registers(items=registers)


@dataclass(kw_only=True)
class Block:
    origin: BlockOrigin
    terminator: Terminator

    # registers: Registers
    # instructions: List[BlockInstruction]
