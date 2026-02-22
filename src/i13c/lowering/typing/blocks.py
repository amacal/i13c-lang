from dataclasses import dataclass
from typing import Set, Union

from i13c.lowering.typing.abstracts import AbstractEntry
from i13c.lowering.typing.flows import FlowEntry
from i13c.lowering.typing.instructions import InstructionEntry
from i13c.lowering.typing.terminators import Terminator
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId

BlockOrigin = Union[FunctionId, SnippetId, CallSiteId]
BlockInstruction = Union[InstructionEntry, AbstractEntry, FlowEntry]


@dataclass
class Registers:
    items: Set[int]

    @staticmethod
    def empty() -> Registers:
        return Registers(items=set())

    @staticmethod
    def instance(registers: Set[int]) -> Registers:
        return Registers(items=registers)


@dataclass
class Block:
    origin: BlockOrigin
    terminator: Terminator

    # registers: Registers
    # instructions: List[BlockInstruction]
