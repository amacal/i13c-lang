from typing import Optional, Union

from i13c.encoding import kind
from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.llvm.typing.instructions.addr import LeaInstruction


def encode_lea_reg_off(
    instruction: LeaInstruction, bytecode: bytearray
) -> Optional[Union[LabelArtifact, RelocationArtifact]]:

    modrm_reg = kind.encode_modrm_reg(instruction.dst)
    modrm_rm = kind.encode_modrm_rm(instruction.src)

    kind.write_rex(bytecode, modrm_reg, modrm_rm)
    kind.write_opcode(bytecode, 1, 0x8D)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)
