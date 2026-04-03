from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, Immediate, ModRM, Opcode, Prefixes
from i13c.llvm.typing.instructions.bits import (
    BSwapInstruction,
    ShlReg8Imm8,
    ShlReg16Imm8,
    ShlReg32Imm8,
    ShlReg64Cl,
    ShlReg64Imm8,
)


def encode_shl_reg_imm(
    instruction: Union[ShlReg8Imm8, ShlReg16Imm8, ShlReg32Imm8, ShlReg64Imm8],
    bytecode: bytearray,
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: 66 + REX + (C0|C1|D0|D1) /4 ib
    # encoded as: [prefixes?] [rex?] [opcode] [modrm] [imm8]

    prefixes = Prefixes(
        operand_override=instruction.dst.width == 16,
    )

    rex = REX(
        w=instruction.dst.width == 64,
        r=False,
        x=False,
        b=instruction.dst.id >= 8,
    )

    if instruction.dst.width == 8:
        value = 0xD0 if instruction.imm.value == 1 else 0xC0
    else:
        value = 0xD1 if instruction.imm.value == 1 else 0xC1

    opcode = Opcode(
        hex=value,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=4,
        rm=instruction.dst.id & 0x07,
    )

    imm8 = Immediate(
        value=instruction.imm.value,
        width=1,
        signed=False,
    )

    bytecode.extend(
        [
            *prefixes.to_bytes(),
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm8.to_bytes(imm8.value > 1),
        ]
    )


def encode_shl_reg_cl(
    instruction: ShlReg64Cl, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + D2 /4
    # encoded as: [rex] [opcode] [modrm]

    rex = REX(
        w=True,
        r=False,
        x=False,
        b=instruction.dst.id >= 8,
    )

    opcode = Opcode(
        hex=0xD2,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=4,
        rm=instruction.dst.id & 0x07,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
        ]
    )


def encode_bswap(
    instruction: BSwapInstruction, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 0F (C8 + rd)
    # encoded as: [rex] [0F] [opcode]

    opcode = Opcode(
        hex=0xC8,
        reg=instruction.dst.id,  # low 3 bits go into opcode
    )

    rex = REX(
        w=instruction.dst.width == 64,
        r=False,
        x=False,
        b=opcode.rex_b(),  # high bit of register
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            0x0F,
            opcode.to_byte(),
        ]
    )
