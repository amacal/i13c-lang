from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, SIB, Displacement, Immediate, ModRM, Opcode
from i13c.llvm.typing.instructions.move import (
    MovOffImm,
    MovOffReg,
    MovRegImm,
    MovRegOff,
    MovRegReg,
)


def encode_mov_reg_imm(
    instruction: MovRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + (B8 + rd) + imm64
    # encoded as: [rex] [opcode] [imm64]

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
        value=int.from_bytes(instruction.imm.data, byteorder="little"),
        width=8,
        signed=False,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            *imm64.to_bytes(),
        ]
    )


def encode_mov_reg_reg(
    instruction: MovRegReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 89 /r
    # encoded as: [rex] [opcode] [modrm]

    modrm = ModRM(
        mod=0b11,
        reg=instruction.src,
        rm=instruction.dst,
    )

    rex = REX(
        w=True,
        r=modrm.rex_r(),
        x=False,
        b=modrm.rex_b(),
    )

    opcode = Opcode(
        hex=0x89,
        reg=None,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
        ]
    )


def encode_mov_off_imm(
    instruction: MovOffImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # will be encoded as single imm32 if possible, otherwise as two moves

    # chosen encoding: REX.W + C7 /0 id
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32] [imm32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.dst.base.id,
    )

    modrm = ModRM(
        mod=0b10,
        reg=0,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=True,  # sign-extend to 64 bits
        r=False,
        x=sib.rex_x(),
        b=modrm.rex_b() or sib.rex_b(),
    )

    opcode = Opcode(
        hex=0xC7,
        reg=None,
    )

    disp32 = Displacement(
        value=int.from_bytes(
            instruction.dst.disp.data, byteorder="little", signed=False
        ),
        width=4,
        signed=True,
    )

    imm32 = Immediate(
        value=int.from_bytes(instruction.imm.data, byteorder="little") & 0xFFFFFFFF,
        width=4,
        signed=False,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *disp32.to_bytes(),
            *imm32.to_bytes(),
        ]
    )


def encode_mov_off_reg(
    instruction: MovOffReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 89 /r
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.dst.base.id,
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

    disp32 = Displacement(
        value=int.from_bytes(
            instruction.dst.disp.data, byteorder="little", signed=False
        ),
        width=4,
        signed=True,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *disp32.to_bytes(),
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
        base=instruction.src.base.id,
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

    disp32 = Displacement(
        value=int.from_bytes(
            instruction.src.disp.data, byteorder="little", signed=False
        ),
        width=4,
        signed=True,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *disp32.to_bytes(),
        ]
    )
