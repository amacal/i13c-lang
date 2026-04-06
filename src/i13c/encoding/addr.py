from i13c.encoding import kind
from i13c.llvm.typing.instructions.addr import LeaInstruction


def encode_lea_reg_off(instruction: LeaInstruction, bytecode: bytearray):
    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(instruction.dst)
    modrm_rm = kind.encode_modrm_rm(instruction.src)

    # derive rex prefix
    rex = kind.encode_rex(instruction.dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # encode instruction
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, 0x8D)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)
