from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, Immediate, ModRM, Opcode
from i13c.llvm.typing.instructions import ByteSwap, ShlRegImm, ShlRegReg


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


def encode_shl_reg_reg(
    instruction: ShlRegReg, bytecode: bytearray
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
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
        ]
    )


def encode_bswap(
    instruction: ByteSwap, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 0F (C8 + rd)
    # encoded as: [rex] [0F] [opcode]

    opcode = Opcode(
        hex=0xC8,
        reg=instruction.target,  # low 3 bits go into opcode
    )

    rex = REX(
        w=True,
        r=False,
        x=False,
        b=opcode.rex_b(),  # high bit of register
    )

    bytecode.extend(
        [
            rex.to_byte(),
            0x0F,
            opcode.to_byte(),
        ]
    )
