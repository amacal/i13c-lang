from typing import Dict, List, Optional, Protocol, Type, Union

from i13c.encoding.bits import encode_shl_reg_imm
from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.jump import (
    encode_call,
    encode_jump,
    encode_label,
    encode_nop,
    encode_return,
    encode_syscall,
)
from i13c.encoding.math import encode_add_reg_imm, encode_sub_reg_imm
from i13c.encoding.mov import (
    encode_mov_off_imm,
    encode_mov_off_reg,
    encode_mov_reg_imm,
    encode_mov_reg_off,
    encode_mov_reg_reg,
)
from i13c.encoding.stack import encode_pop_off, encode_push_off
from i13c.llvm.typing.instructions import (
    AddRegImm,
    Call,
    Instruction,
    Jump,
    Label,
    MovOffImm,
    MovOffReg,
    MovRegImm,
    MovRegOff,
    MovRegReg,
    Nop,
    PopOff,
    PushOff,
    Return,
    ShlRegImm,
    SubRegImm,
    SysCall,
)


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
    MovRegImm: encode_mov_reg_imm,
    MovRegReg: encode_mov_reg_reg,
    MovOffImm: encode_mov_off_imm,
    MovOffReg: encode_mov_off_reg,
    MovRegOff: encode_mov_reg_off,
    PushOff: encode_push_off,
    PopOff: encode_pop_off,
    ShlRegImm: encode_shl_reg_imm,
    SubRegImm: encode_sub_reg_imm,
    AddRegImm: encode_add_reg_imm,
    SysCall: encode_syscall,
    Return: encode_return,
    Label: encode_label,
    Call: encode_call,
    Jump: encode_jump,
    Nop: encode_nop,
}  # pyright: ignore[reportAssignmentType]
