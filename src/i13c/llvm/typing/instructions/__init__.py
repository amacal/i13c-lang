from dataclasses import dataclass
from typing import Tuple, Union

from i13c.llvm.typing.instructions import addr, bits, jump, math, move, stack

Instruction = Union[
    addr.LeaReg32Off,
    addr.LeaReg64Off,
    bits.ByteSwapReg32,
    bits.ByteSwapReg64,
    bits.ShlRegImm,
    bits.ShlRegReg,
    jump.Call,
    jump.Jump,
    jump.Label,
    jump.Nop,
    jump.Nop,
    jump.Return,
    jump.SysCall,
    math.AddRegImm,
    math.AddRegReg,
    math.SubRegImm,
    move.MovOffImm,
    move.MovOffReg,
    move.MovRegImm,
    move.MovRegOff,
    move.MovRegReg,
    stack.PopOff,
    stack.PushOff,
]


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


InstructionEntry = Tuple[InstructionId, Instruction]
