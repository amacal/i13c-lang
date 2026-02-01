from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Type, Union

from i13c.encoding.core import REX, SIB, Immediate, ModRM, Opcode
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

    # chosen encoding: REX.W + (B8 + rd) + imm64
    # encoded as: [rex] [opcode] [imm64]

    # in this encoding, the low 3 bits of the register are encoded in the opcode,
    # while the high bit is encoded in the REX.B field

    opcode = Opcode(
        hex=0xB8,
        reg=instruction.dst,
    )

    rex = REX(
        w=True,
        r=False,
        x=False,
        b=opcode.rex_b(),
    )

    imm64 = Immediate(
        value=instruction.imm,
        width=8,
        signed=False,
    )

    bytecode.extend([rex.to_byte(), opcode.to_byte(), *imm64.to_bytes()])


def encode_mov_off_reg(
    instruction: MovOffReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 89 /r
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.dst,
    )

    modrm = ModRM(
        mod=0b10,
        reg=instruction.src,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=True,
        r=modrm.rex_r(),
        x=sib.rex_x(),
        b=modrm.rex_b() or sib.rex_b(),
    )

    opcode = Opcode(
        hex=0x89,
        reg=None,
    )

    imm32 = Immediate(
        value=instruction.off,
        width=4,
        signed=True,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *imm32.to_bytes(),
        ]
    )


def encode_mov_reg_off(
    instruction: MovRegOff, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 8B /r
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.src,
    )

    modrm = ModRM(
        mod=0b10,
        reg=instruction.dst,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=True,
        r=modrm.rex_r(),
        x=sib.rex_x(),
        b=modrm.rex_b() or sib.rex_b(),
    )

    opcode = Opcode(
        hex=0x8B,
        reg=None,
    )

    imm32 = Immediate(
        value=instruction.off,
        width=4,
        signed=True,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *imm32.to_bytes(),
        ]
    )


def encode_shl_reg_imm(
    instruction: ShlRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + C1 /4 ib
    # encoded as: [rex] [opcode] [modrm] [imm8]

    rex = REX(
        w=True,
        r=False,
        x=False,
        b=instruction.dst >= 8,
    )

    opcode = Opcode(
        hex=0xC1,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=4,
        rm=instruction.dst & 0x07,
    )

    imm8 = Immediate(
        value=instruction.imm,
        width=1,
        signed=False,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm8.to_bytes(),
        ]
    )


def encode_sub_reg_imm(
    instruction: SubRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 81 /5 id
    # encoded as: [rex] [opcode] [modrm] [imm32]

    rex = REX(
        w=True,
        r=False,
        x=False,
        b=instruction.dst >= 8,
    )

    opcode = Opcode(
        hex=0x81,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=5,
        rm=instruction.dst & 0x07,
    )

    imm32 = Immediate(
        value=instruction.imm,
        width=4,
        signed=False,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm32.to_bytes(),
        ]
    )


def encode_add_reg_imm(
    instruction: AddRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 81 /0 id
    # encoded as: [rex] [opcode] [modrm] [imm32]

    rex = REX(
        w=True,
        r=False,
        x=False,
        b=instruction.dst >= 8,
    )

    opcode = Opcode(
        hex=0x81,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=0,
        rm=instruction.dst & 0x07,
    )

    imm32 = Immediate(
        value=instruction.imm,
        width=4,
        signed=False,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm32.to_bytes(),
        ]
    )


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
