from i13c.encoding import kind
from i13c.llvm.typing.instructions.bits import BSwapReg, ShlRegImm, ShlRegReg


def encode_shl_reg_imm(instruction: ShlRegImm, bytecode: bytearray) -> None:
    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(0x04)
    modrm_rm = kind.encode_modrm_rm(instruction.dst)

    # derive prefixes and rex
    prefixes = kind.encode_prefixes(instruction.dst)
    rex = kind.encode_rex(instruction.dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # determine if imm8 encoding is needed
    needs_imm8 = instruction.imm.value != 1

    # determine opcode based on operand size
    if needs_imm8:
        opcode = 0xC0 if instruction.dst.is_8bit() else 0xC1
    else:
        opcode = 0xD0 if instruction.dst.is_8bit() else 0xD1

    # encode instruction
    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, opcode)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)
    kind.write_immediate(bytecode, instruction.imm, condition=needs_imm8, signed=False)


def encode_shl_reg_cl(instruction: ShlRegReg, bytecode: bytearray) -> None:
    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(0x04)
    modrm_rm = kind.encode_modrm_rm(instruction.dst)

    # derive prefixes and rex
    prefixes = kind.encode_prefixes(instruction.dst)
    rex = kind.encode_rex(instruction.dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # determine opcode based on operand size
    opcode = 0xD2 if instruction.dst.is_8bit() else 0xD3

    # encode instruction
    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, opcode)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)


def encode_bswap(instruction: BSwapReg, bytecode: bytearray) -> None:
    # derive opcode and rex
    opcode_reg = kind.encode_opcode_reg(instruction.dst)
    rex = kind.encode_rex(instruction.dst, opcode_reg=opcode_reg)

    # encode instruction
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 2, 0x0FC8, opcode_reg=opcode_reg)
