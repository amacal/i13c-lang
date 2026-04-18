from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.semantic.typing.entities.operands import OperandId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Instruction:
    ref: Span
    mnemonic: MnemonicId
    operands: List[OperandId]

    def __str__(self) -> str:
        operands = ":".join(op.identify(2) for op in self.operands)
        return f"{self.mnemonic.identify(1)}, operands={operands}"
