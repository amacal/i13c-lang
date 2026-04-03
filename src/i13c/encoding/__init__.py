from typing import Dict, List, Optional, Protocol, Type, Union

from i13c.encoding import addr, bits, ctrl, math, move, stack
from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.llvm.typing import instructions as llvm
from i13c.llvm.typing.instructions import Instruction


class MissingLabelError(Exception):
    def __init__(self, target: int) -> None:
        self.target = target
        super().__init__(f"missing target label for relocation {target}")


class DuplicateLabelError(Exception):
    def __init__(self, target: int) -> None:
        self.target = target
        super().__init__(f"duplicate label with id {target}")


def encode(instructions: List[Instruction]) -> bytes:
    bytecode = bytearray()
    labels: Dict[int, LabelArtifact] = {}
    relocations: List[RelocationArtifact] = []

    for instruction in instructions:
        if artifact := DISPATCH_TABLE[type(instruction)](instruction, bytecode):
            if isinstance(artifact, LabelArtifact):
                # check for duplicate labels
                if artifact.target in labels:
                    raise DuplicateLabelError(artifact.target)

                labels[artifact.target] = artifact
            else:
                relocations.append(artifact)

    for relocation in relocations:
        if relocation.target not in labels:
            raise MissingLabelError(relocation.target)

        target = labels[relocation.target].offset - (relocation.offset + 4)
        low, high = relocation.offset, relocation.offset + 4

        bytecode[low:high] = target.to_bytes(4, byteorder="little", signed=True)

    return bytes(bytecode)


class Encoder(Protocol):
    def __call__(
        self, instruction: Instruction, out: bytearray
    ) -> Optional[Union[LabelArtifact, RelocationArtifact]]: ...


DISPATCH_TABLE: Dict[Type[Instruction], Encoder] = {
    llvm.addr.LeaReg32Mem: addr.encode_lea_reg_off,
    llvm.addr.LeaReg64Mem: addr.encode_lea_reg_off,
    llvm.bits.ByteSwapReg32: bits.encode_bswap,
    llvm.bits.ByteSwapReg64: bits.encode_bswap,
    llvm.bits.ShlReg8Imm8: bits.encode_shl_reg_imm,
    llvm.bits.ShlReg16Imm8: bits.encode_shl_reg_imm,
    llvm.bits.ShlReg32Imm8: bits.encode_shl_reg_imm,
    llvm.bits.ShlReg64Imm8: bits.encode_shl_reg_imm,
    llvm.bits.ShlReg8Cl: bits.encode_shl_reg_cl,
    llvm.bits.ShlReg16Cl: bits.encode_shl_reg_cl,
    llvm.bits.ShlReg32Cl: bits.encode_shl_reg_cl,
    llvm.bits.ShlReg64Cl: bits.encode_shl_reg_cl,
    llvm.ctrl.Call: ctrl.encode_call,
    llvm.ctrl.Jump: ctrl.encode_jump,
    llvm.ctrl.Label: ctrl.encode_label,
    llvm.ctrl.Nop: ctrl.encode_nop,
    llvm.ctrl.Return: ctrl.encode_return,
    llvm.ctrl.SysCall: ctrl.encode_syscall,
    llvm.math.AddRegImm: math.encode_add_reg_imm,
    llvm.math.AddRegReg: math.encode_add_reg_reg,
    llvm.math.SubRegImm: math.encode_sub_reg_imm,
    llvm.move.MovOffImm: move.encode_mov_off_imm,
    llvm.move.MovOffReg: move.encode_mov_off_reg,
    llvm.move.MovRegImm: move.encode_mov_reg_imm,
    llvm.move.MovRegOff: move.encode_mov_reg_off,
    llvm.move.MovRegReg: move.encode_mov_reg_reg,
    llvm.stack.PopOff: stack.encode_pop_off,
    llvm.stack.PushOff: stack.encode_push_off,
}  # pyright: ignore[reportAssignmentType]
