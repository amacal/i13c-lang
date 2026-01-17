from dataclasses import dataclass
from typing import List, Union

from i13c.lowering.typing.flows import Flow
from i13c.lowering.typing.instructions import Instruction
from i13c.lowering.typing.terminators import Terminator
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import SnippetId

BlockOrigin = Union[FunctionId, SnippetId, CallSiteId]
BlockInstruction = Union[Instruction, Flow]


@dataclass
class Block:
    origin: BlockOrigin
    terminator: Terminator
    instructions: List[BlockInstruction]

    def describe(self) -> str:
        return f"origin={self.origin.identify(2)}, instrs={len(self.instructions)}, term={self.terminator}"
