from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, SIB, Displacement, ModRM, Opcode
from i13c.llvm.typing.instructions.addr import LeaRegOff


def encode_lea_reg_off(
    instruction: LeaRegOff, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + 8D /r
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.src,
    )

    modrm = ModRM(
        mod=0b10,  # disp32
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
        hex=0x8D,
        reg=None,
    )

    disp32 = Displacement(
        value=instruction.off,
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
