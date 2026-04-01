from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, Immediate, ModRM, Opcode
from i13c.llvm.typing.instructions import (
    AddRegImm,
    AddRegReg,
    SubRegImm,
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
            *rex.to_bytes(),
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
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *imm32.to_bytes(),
        ]
    )


def encode_add_reg_reg(
    instruction: AddRegReg, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 01 /r
    # encoded as: [rex] [opcode] [modrm]

    rex = REX(
        w=True,
        r=instruction.src >= 8,
        x=False,
        b=instruction.dst >= 8,
    )

    opcode = Opcode(
        hex=0x01,
        reg=None,
    )

    modrm = ModRM(
        mod=0b11,
        reg=instruction.src & 0x07,  # source register
        rm=instruction.dst & 0x07,  # destination register
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
        ]
    )
