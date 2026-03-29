from typing import Optional, Union

from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.encoding.intel import REX, SIB, Displacement, ModRM, Opcode
from i13c.llvm.typing.instructions import PopOff, PushOff


def encode_push_off(
    instruction: PushOff, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + FF /6
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.src,
    )

    modrm = ModRM(
        mod=0b10,
        reg=6,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=False,  # ignored
        r=False,
        x=sib.rex_x(),
        b=modrm.rex_b() or sib.rex_b(),
    )

    opcode = Opcode(
        hex=0xFF,
        reg=None,
    )

    disp32 = Displacement(
        value=instruction.off,
        width=4,
        signed=True,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *disp32.to_bytes(),
        ]
    )


def encode_pop_off(
    instruction: PopOff, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    # chosen encoding: REX.W + FF /0
    # encoded as: [rex] [opcode] [modrm] [sib?] [disp32]

    sib = SIB(
        scale=0,
        index=None,
        base=instruction.dst,
    )

    modrm = ModRM(
        mod=0b10,
        reg=0,
        rm=sib.mod_rm(),
    )

    rex = REX(
        w=False,  # ignored
        r=False,
        x=sib.rex_x(),
        b=modrm.rex_b() or sib.rex_b(),
    )

    opcode = Opcode(
        hex=0x8F,
        reg=None,
    )

    disp32 = Displacement(
        value=instruction.off,
        width=4,
        signed=True,
    )

    bytecode.extend(
        [
            rex.to_byte(),
            opcode.to_byte(),
            modrm.to_byte(),
            *sib.to_bytes(),
            *disp32.to_bytes(),
        ]
    )
