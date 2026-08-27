from i13c.encoding import kind
from i13c.encoding.kind import ImmediateInfo, RegisterInfo
from i13c.semantic.typing.analyses.llvm import BSWAP, SHL, SHR, Immediate, Register


def encode_shl(instruction: SHL, bytecode: bytearray) -> None:
    return encode_shift(0x04, instruction, bytecode)


def encode_shr(instruction: SHR, bytecode: bytearray) -> None:
    return encode_shift(0x05, instruction, bytecode)


def encode_shift(extension: int, instruction: SHL | SHR, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume no immediate value for now
    immediate: Immediate | None = None

    # only register can be 8-bit, memory operands are always 64-bit
    is_8bit = isinstance(dst, Register) and RegisterInfo.is_8bit(dst)

    # the shift stored in CL has to be handled explicitly
    if isinstance(src, Register):
        opcode = 0xD2 if is_8bit else 0xD3

    # the same about the immediate value of 1, which has a dedicated encoding
    elif ImmediateInfo.is_one(src):
        opcode = 0xD0 if is_8bit else 0xD1

    # otherwise fallback to the a bit longer imm8 encoding
    else:
        opcode = 0xC0 if is_8bit else 0xC1
        immediate = src

    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(extension)
    modrm_rm = kind.encode_modrm_rm(dst)

    # derive prefixes and rex
    prefixes = kind.encode_prefixes(dst)
    rex = kind.encode_rex(dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # encode instruction
    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, opcode)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)
    kind.write_immediate(bytecode, immediate, condition=immediate is not None)


def encode_bswap(instruction: BSWAP, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # derive opcode and rex
    opcode_reg = kind.encode_opcode_reg(target)
    rex = kind.encode_rex(target, opcode_reg=opcode_reg)

    # encode instruction
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 2, 0x0FC8, opcode_reg=opcode_reg)
