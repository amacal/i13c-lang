from typing import Optional, Union

from i13c.encoding.core import (
    LabelArtifact,
    RelocationArtifact,
    UnreachableEncodingError,
)
from i13c.encoding.intel import REX, SIB, Displacement, ModRM, Opcode
from i13c.llvm.typing.instructions.addr import LeaInstruction


def encode_lea_reg_off(
    instruction: LeaInstruction, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # encoded as: [rex?] [opcode] [modrm] [sib?] [disp8/32?]

    if instruction.addr.scaler.uses_rsp_r12():
        raise UnreachableEncodingError()

    sib = SIB(
        scale=instruction.addr.scaler.scale_offset(),
        index=instruction.addr.scaler.index_or_none(),
        base=instruction.addr.base.id,
    )

    if instruction.addr.disp.width == 0 and instruction.addr.base.low3bits() != 5:
        mod = 0b00
        disp_width = 0
    elif instruction.addr.disp.width <= 8:  # disp0 with rbp/r13 or disp8
        mod = 0b01
        disp_width = 1
    else:
        mod = 0b10
        disp_width = 4

    modrm = ModRM(
        mod=mod,
        reg=instruction.dst.id,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=instruction.dst.width == "64bit",
        r=modrm.rex_r(),
        x=sib.rex_x(),
        b=modrm.rex_b() or sib.rex_b(),
    )

    opcode = Opcode(
        hex=0x8D,
        reg=None,
    )

    disp = Displacement(
        value=instruction.addr.disp.value,
        width=disp_width,
        signed=True,
    )

    bytecode.extend(
        [
            *rex.to_bytes(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *disp.to_bytes(),
        ]
    )
