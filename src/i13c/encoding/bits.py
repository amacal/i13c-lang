from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, Immediate, ModRM, Opcode, Prefixes
from i13c.llvm.typing.instructions.bits import BSwapReg, ShlRegImm, ShlRegReg


def encode_shl_reg_imm(
    instruction: ShlRegImm, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: 66 + REX + (C0|C1|D0|D1) /4 ib
    # encoded as: [prefixes?] [rex?] [opcode] [modrm] [imm8]

    prefixes = Prefixes(
        operand_override=instruction.dst.width == "16bit",
    )

    rex = REX(
        w=instruction.dst.width == "64bit",
        r=False,
        x=False,
        b=instruction.dst.id >= 8,
    )

    if instruction.dst.width in ("low", "high", "8bit"):
        opcode_value = 0xD0 if instruction.imm.value == 1 else 0xC0
    else:
        opcode_value = 0xD1 if instruction.imm.value == 1 else 0xC1

    if instruction.dst.width in ("low") and instruction.dst.id in (4, 5, 6, 7):
        rex_force = True
    else:
        rex_force = False

    opcode = Opcode(
        hex=opcode_value,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=4,
        rm=instruction.dst.low3bits(),
    )

    imm8 = Immediate(
        value=instruction.imm.value,
        width=1,
        signed=False,
    )

    bytecode.extend(
        [
            *prefixes.to_bytes(),
            *rex.to_bytes(force=rex_force),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm8.to_bytes(imm8.value > 1),
        ]
    )


def encode_shl_reg_cl(
    instruction: ShlRegReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: 66 REX.W + (D2/D3) /4
    # encoded as: [prefixes?] [rex?] [opcode] [modrm]

    prefixes = Prefixes(
        operand_override=instruction.dst.width == "16bit",
    )

    rex = REX(
        w=instruction.dst.width == "64bit",
        r=False,
        x=False,
        b=instruction.dst.id >= 8,
    )

    if instruction.dst.width in ("low", "high", "8bit"):
        opcode_value = 0xD2
    else:
        opcode_value = 0xD3

    if instruction.dst.width in ("low") and instruction.dst.id in (4, 5, 6, 7):
        rex_force = True
    else:
        rex_force = False

    opcode = Opcode(
        hex=opcode_value,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=4,
        rm=instruction.dst.low3bits(),
    )

    bytecode.extend(
        [
            *prefixes.to_bytes(),
            *rex.to_bytes(force=rex_force),
            opcode.to_byte(),
            modrm.to_byte(),
        ]
    )


def encode_bswap(
    instruction: BSwapReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 0F (C8 + rd)
    # encoded as: [rex] [0F] [opcode]

    opcode = Opcode(
        hex=0xC8,
        reg=instruction.dst.id,  # low 3 bits go into opcode
    )

    rex = REX(
        w=instruction.dst.width == "64bit",
        r=False,
        x=False,
        b=opcode.rex_b(),
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            0x0F,
            opcode.to_byte(),
        ]
    )
