from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, SIB, Displacement, ModRM, Opcode
from i13c.llvm.typing.instructions.addr import LeaReg32Off, LeaReg64Off


def encode_lea_reg_off(
    instruction: Union[LeaReg32Off, LeaReg64Off], bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # encoded as: [rex] [opcode] [modrm] [sib?] [disp8/32?]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.src,
    )

    if instruction.off == 0 and (instruction.src & 0b111) != 5:  # rbp/r13
        mod = 0b00
        disp_width = 0
    elif -128 <= instruction.off <= 127:
        mod = 0b01
        disp_width = 1
    else:
        mod = 0b10
        disp_width = 4

    modrm = ModRM(
        mod=mod,
        reg=instruction.dst,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=isinstance(instruction, LeaReg64Off),
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
        width=disp_width,
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
