from typing import Optional, Union

from i13c.encoding.core import (
    Address,
    LabelArtifact,
    RelocationArtifact,
    UnreachableEncodingError,
)
from i13c.encoding.intel import REX, SIB, Displacement, ModRM, Opcode
from i13c.llvm.typing.instructions.addr import LeaInstruction


def encode_lea_reg_off(
    instruction: LeaInstruction, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    if Address.index_uses_rsp(instruction.addr):
        raise UnreachableEncodingError()

    sib = SIB(
        scale=Address.scale_offset(instruction.addr),
        index=Address.index_or_none(instruction.addr),
        base=Address.base_or_none(instruction.addr),
    )

    if Address.is_relative(instruction.addr):
        modrm_mod = 0b00
        disp_width = 4
    elif instruction.addr.disp.width == 0 and not Address.base_uses_rbp_r13(instruction.addr):
        modrm_mod = 0b00
        disp_width = 0
    elif instruction.addr.disp.width <= 8:  # disp0 with rbp/r13 or disp8
        modrm_mod = 0b01
        disp_width = 1
    else:
        modrm_mod = 0b10
        disp_width = 4

    if not Address.base_is_available(instruction.addr):
        disp_width = max(disp_width, 4)

    modrm = ModRM(
        mod=modrm_mod,
        reg=instruction.dst.id,
        rm=0b101 if Address.is_relative(instruction.addr) else sib.mod_rm(),
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
