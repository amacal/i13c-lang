from dataclasses import dataclass

from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.analyses.fnlets import FnletInstruction
from i13c.semantic.typing.analyses.llvm import (
    AND,
    BSWAP,
    CALL,
    JMP,
    LEA,
    LOOP,
    MOV,
    NOP,
    OR,
    RET,
    SHL,
    SHR,
    SYSCALL,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span

AsmletInstruction = (
    AND | BSWAP | CALL | JMP | LEA | LOOP | MOV | NOP | OR | RET | SHL | SHR | SYSCALL
)

BlockletTarget = FunctionId | AsmletId
BlockletInstruction = FnletInstruction | AsmletInstruction


@dataclass(kw_only=True, frozen=True)
class BlockletId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("blocklet", f"{self.value:<{length}}"))


@dataclass(kw_only=True, repr=False)
class BlockletBlock:
    instructions: list[BlockletInstruction]

    def listing(self) -> list[str]:
        return [str(instruction) for instruction in self.instructions]


@dataclass(kw_only=True, repr=False)
class Blocklet:
    ref: Span
    id: BlockletId

    target: BlockletTarget
    blocks: list[BlockletBlock]

    def listing(self) -> list[str]:
        return [
            str(instruction)
            for block in self.blocks
            for instruction in block.instructions
        ]
