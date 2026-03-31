from typing import Dict, List, Optional, Protocol, Type, Union

from i13c.encoding import addr, bits, jump, math, move, stack
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
    llvm.AddRegImm: math.encode_add_reg_imm,
    llvm.AddRegReg: math.encode_add_reg_reg,
    llvm.ByteSwap: bits.encode_bswap,
    llvm.Call: jump.encode_call,
    llvm.Jump: jump.encode_jump,
    llvm.Label: jump.encode_label,
    llvm.LeaRegOff: addr.encode_lea_reg_off,
    llvm.MovOffImm: move.encode_mov_off_imm,
    llvm.MovOffReg: move.encode_mov_off_reg,
    llvm.MovRegImm: move.encode_mov_reg_imm,
    llvm.MovRegOff: move.encode_mov_reg_off,
    llvm.MovRegReg: move.encode_mov_reg_reg,
    llvm.Nop: jump.encode_nop,
    llvm.PopOff: stack.encode_pop_off,
    llvm.PushOff: stack.encode_push_off,
    llvm.Return: jump.encode_return,
    llvm.ShlRegImm: bits.encode_shl_reg_imm,
    llvm.ShlRegReg: bits.encode_shl_reg_reg,
    llvm.SubRegImm: math.encode_sub_reg_imm,
    llvm.SysCall: jump.encode_syscall,
}  # pyright: ignore[reportAssignmentType]
