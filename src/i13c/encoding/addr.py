from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo
from i13c.semantic.typing.analyses.llvm import LEA, Relocation


def encode_lea(instruction: LEA, bytecode: bytearray) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(dst)
    modrm_rm = kind.encode_modrm_rm(src)

    # derive prefixes and rex
    prefixes = kind.encode_prefixes(dst)
    rex = kind.encode_rex(dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # encode instruction
    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, 0x8D)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)

    if not isinstance(src.disp, Relocation):
        return None

    return RelocationInfo(
        target=src.disp.block,
        offset=len(bytecode) - 4,
        width=4,
    )
