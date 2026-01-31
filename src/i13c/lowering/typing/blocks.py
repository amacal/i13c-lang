from dataclasses import dataclass
from typing import List, Set, Union

from i13c.lowering.typing.flows import Flow
from i13c.lowering.typing.instructions import Instruction
from i13c.lowering.typing.terminators import Terminator
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import SnippetId

BlockOrigin = Union[FunctionId, SnippetId, CallSiteId]
BlockInstruction = Union[Instruction, Flow]


@dataclass
class Registers:
    generated: Set[int]
    clobbered: Set[int]

    inputs: Set[int]
    outputs: Set[int]

    @staticmethod
    def empty() -> Registers:
        return Registers(
            generated=set(),
            clobbered=set(),
            inputs=set(),
            outputs=set(),
        )

    @staticmethod
    def provides(registers: Set[int]) -> Registers:
        return Registers(
            generated=set(),
            clobbered=set(),
            inputs=registers,
            outputs=set(),
        )

    @staticmethod
    def clobbers(registers: Set[int]) -> Registers:
        return Registers(
            generated=set(),
            clobbered=registers,
            inputs=set(),
            outputs=set(),
        )


@dataclass
class Block:
    origin: BlockOrigin
    terminator: Terminator

    registers: Registers
    instructions: List[BlockInstruction]

    def describe(self) -> str:
        return f"origin={self.origin.identify(2)}, instrs={len(self.instructions)}, term={self.terminator}"
