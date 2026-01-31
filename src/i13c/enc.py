from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Type, Union

from i13c.lowering.typing.instructions import (
    AddRegImm,
    Call,
    Instruction,
    Label,
    MovOffReg,
    MovRegImm,
    MovRegOff,
    Return,
    ShlRegImm,
    SubRegImm,
    SysCall,
)


def encode(instructions: List[Instruction]) -> bytes:
    bytecode = bytearray()
    labels: Dict[int, LabelArtifact] = {}
    relocations: List[RelocationArtifact] = []

    for instruction in instructions:
        if artifact := DISPATCH_TABLE[type(instruction)](instruction, bytecode):
            if isinstance(artifact, LabelArtifact):
                labels[artifact.target] = artifact
            else:
                relocations.append(artifact)

    for relocation in relocations:
        target = labels[relocation.target].offset - (relocation.offset + 4)
        low, high = relocation.offset, relocation.offset + 4

        bytecode[low:high] = target.to_bytes(4, byteorder="little", signed=True)

    return bytes(bytecode)


def encode_mov_reg_imm(
    instruction: MovRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # REX.W + B8+rd io
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xB8 | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(8, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, *imm])


def encode_mov_off_reg(
    instruction: MovOffReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # REX.W + 89 /r
    rex = (
        0x40
        | 0x08
        | (0x04 if instruction.src >= 8 else 0x00)
        | (0x01 if instruction.dst >= 8 else 0x00)
    )

    opcode = 0x89
    modrm = 0x80 | ((instruction.src & 0x07) << 3) | (instruction.dst & 0x07)

    # append REX, opcode, modrm
    bytecode.extend([rex, opcode, modrm])

    # handle SIB for RSP
    if (instruction.dst & 0x07) == 4:
        bytecode.append((0 << 6) | (4 << 3) | (instruction.dst & 0x07))

    # append 32-bit offset
    bytecode.extend(instruction.off.to_bytes(4, byteorder="little", signed=True))


def encode_mov_reg_off(
    instruction: MovRegOff, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # REX.W + 89 /r
    rex = (
        0x40
        | 0x08
        | (0x04 if instruction.dst >= 8 else 0x00)
        | (0x01 if instruction.src >= 8 else 0x00)
    )

    opcode = 0x8B
    modrm = 0x80 | ((instruction.dst & 0x07) << 3) | (instruction.src & 0x07)

    # append REX, opcode, modrm
    bytecode.extend([rex, opcode, modrm])

    # handle SIB for RSP
    if (instruction.src & 0x07) == 4:
        bytecode.append((0 << 6) | (4 << 3) | (instruction.src & 0x07))

    # append 32-bit offset
    bytecode.extend(instruction.off.to_bytes(4, byteorder="little", signed=True))


def encode_shl_reg_imm(
    instruction: ShlRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # REX.W + C1 /4 ib
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xC1
    modrm = 0xE0 | (4 << 3) | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(1, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, modrm, *imm])


def encode_sub_reg_imm(
    instruction: SubRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # REX.W + 81 /5 id
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0x81
    modrm = 0xE0 | (5 << 3) | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(4, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, modrm, *imm])


def encode_add_reg_imm(
    instruction: AddRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # REX.W + 81 /0 id
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0x81
    modrm = 0xC0 | (0 << 3) | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(4, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, modrm, *imm])


def encode_syscall(
    instruction: SysCall, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    bytecode.extend([0x0F, 0x05])


def encode_return(
    instruction: Return, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # C3 is simply RET
    bytecode.extend([0xC3])


def encode_label(
    instruction: Label, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # record label position
    offset = len(bytecode)
    target = instruction.id.value

    # the label points at the current bytecode length
    return LabelArtifact(target=target, offset=offset)


def encode_call(
    instruction: Call, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:
    # emit E8 cd --- where cd is a signed 32-bit offset
    bytecode.extend([0xE8, 0x00, 0x00, 0x00, 0x00])

    # record relocation info
    offset = len(bytecode) - 4
    target = instruction.target.value

    # record relocation to be fixed up later
    return RelocationArtifact(target=target, offset=offset)


@dataclass(kw_only=True)
class LabelArtifact:
    target: int
    offset: int


@dataclass(kw_only=True)
class RelocationArtifact:
    target: int
    offset: int


class Encoder(Protocol):
    def __call__(
        self, instruction: Instruction, out: bytearray
    ) -> Optional[Union[LabelArtifact, RelocationArtifact]]: ...


DISPATCH_TABLE: Dict[Type[Instruction], Encoder] = {
    MovRegImm: encode_mov_reg_imm,
    MovOffReg: encode_mov_off_reg,
    MovRegOff: encode_mov_reg_off,
    ShlRegImm: encode_shl_reg_imm,
    SubRegImm: encode_sub_reg_imm,
    AddRegImm: encode_add_reg_imm,
    SysCall: encode_syscall,
    Return: encode_return,
    Label: encode_label,
    Call: encode_call,
}  # pyright: ignore[reportAssignmentType]
