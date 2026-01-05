from dataclasses import dataclass
from typing import List, Union

from i13c.ir import Instruction, Terminator
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import SnippetId


@dataclass(kw_only=True, frozen=True)
class BlockId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("block", f"{self.value:<{length}}"))


BlockOrigin = Union[FunctionId, SnippetId, CallSiteId]


@dataclass
class Block:
    origin: BlockOrigin
    terminator: Terminator
    instructions: List[Instruction]

    def describe(self) -> str:
        return f"origin={self.origin.identify(2)}, instrs={len(self.instructions)}, term={self.terminator}"
