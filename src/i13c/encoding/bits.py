from typing import Optional

from i13c.encoding import kind
from i13c.llvm.typing.instructions.bits import BSWAP, SHL
from i13c.llvm.typing.instructions.core import Immediate, Register


def encode_shl(instruction: SHL, bytecode: bytearray) -> None:
    immediate: Optional[Immediate] = None

    # the shift stored in CL has to be handled explicitly
    if isinstance(instruction.src, Register):
        opcode = 0xD2 if instruction.dst.is_8bit() else 0xD3

    # the same about the immediate value of 1, which has a dedicated encoding
    elif instruction.src.value == 0x01:
        opcode = 0xD0 if instruction.dst.is_8bit() else 0xD1

    # otherwise fallback to the a bit longer imm8 encoding
    else:
        opcode = 0xC0 if instruction.dst.is_8bit() else 0xC1
        immediate = instruction.src

    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(0x04)
    modrm_rm = kind.encode_modrm_rm(instruction.dst)

    # derive prefixes and rex
    prefixes = kind.encode_prefixes(instruction.dst)
    rex = kind.encode_rex(instruction.dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # encode instruction
    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, opcode)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)
    kind.write_immediate(bytecode, immediate, condition=immediate is not None, signed=False)


def encode_bswap(instruction: BSWAP, bytecode: bytearray) -> None:
    # derive opcode and rex
    opcode_reg = kind.encode_opcode_reg(instruction.dst)
    rex = kind.encode_rex(instruction.dst, opcode_reg=opcode_reg)

    # encode instruction
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 2, 0x0FC8, opcode_reg=opcode_reg)
