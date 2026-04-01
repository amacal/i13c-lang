from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, Immediate, ModRM, Opcode, Prefixes
from i13c.llvm.typing.instructions.bits import (
    ByteSwapReg32,
    ByteSwapReg64,
    ShlReg8Imm8,
    ShlReg16Imm8,
    ShlReg32Imm8,
    ShlReg64Cl,
    ShlReg64Imm8,
)


def encode_shl_reg_imm(
    instruction: Union[ShlReg8Imm8, ShlReg16Imm8, ShlReg32Imm8, ShlReg64Imm8], bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: 66 + REX + C0|C1 /4 ib
    # encoded as: [prefixes?][rex?] [opcode] [modrm] [imm8]

    prefixes = Prefixes(
        operand_override=isinstance(instruction, ShlReg16Imm8),
    )

    rex = REX(
        w=isinstance(instruction, ShlReg64Imm8),
        r=False,
        x=False,
        b=instruction.dst >= 8,
    )

    opcode = Opcode(
        hex=0xC1 if not isinstance(instruction, ShlReg8Imm8) else 0xC0,
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
            *prefixes.to_bytes(),
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm8.to_bytes(),
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
        b=instruction.dst >= 8,
    )

    opcode = Opcode(
        hex=0xD2,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=4,
        rm=instruction.dst & 0x07,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
        ]
    )


def encode_bswap(
    instruction: Union[ByteSwapReg32, ByteSwapReg64], bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 0F (C8 + rd)
    # encoded as: [rex] [0F] [opcode]

    opcode = Opcode(
        hex=0xC8,
        reg=instruction.target,  # low 3 bits go into opcode
    )

    rex = REX(
        w=isinstance(instruction, ByteSwapReg64),
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
