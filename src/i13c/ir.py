from dataclasses import dataclass
from typing import List, Union

from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import SnippetId


@dataclass
class FallThrough:
    pass


@dataclass
class Stop:
    pass


@dataclass
class Exit:
    pass


Terminator = Union[FallThrough, Stop, Exit]


@dataclass
class MovRegImm:
    dst: int
    imm: int


@dataclass
class ShlRegImm:
    dst: int
    imm: int


@dataclass
class SysCall:
    pass


@dataclass
class Call:
    target: Union[FunctionId, BlockId]


@dataclass
class Return:
    pass


Instruction = Union[MovRegImm, ShlRegImm, SysCall, Call, Return]


@dataclass
class Label:
    id: int


@dataclass
class Jump:
    target: int


InstructionFlow = Union[Instruction, Label, Jump]


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
