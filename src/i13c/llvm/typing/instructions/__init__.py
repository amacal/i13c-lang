#  noqa: F401

from dataclasses import dataclass
from typing import Tuple, Union

from i13c.llvm.typing.instructions import addr, bits, ctrl, math, move, stack

Instruction = Union[
    addr.LEA,
    bits.BSWAP,
    bits.SHL,
    ctrl.Call,
    ctrl.Jump,
    ctrl.Label,
    ctrl.Nop,
    ctrl.Call,
    ctrl.Jump,
    ctrl.Label,
    ctrl.Nop,
    ctrl.Nop,
    ctrl.Return,
    ctrl.SysCall,
    math.AddRegImm,
    math.AddRegReg,
    math.SUB,
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
