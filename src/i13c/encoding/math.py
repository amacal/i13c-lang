from typing import Optional

from i13c.encoding import kind
from i13c.llvm.typing.instructions.core import Address, Immediate, Register
from i13c.llvm.typing.instructions.math import SUB, AddRegImm, AddRegReg

MI = {
    (8, 8): 0x80,
    (16, 16): 0x81,
    (32, 32): 0x81,
    (64, 32): 0x81,
    (16, 8): 0x83,
    (32, 8): 0x83,
    (64, 8): 0x83,
}

MR = {
    (8, 8): 0x28,
    (16, 16): 0x29,
    (32, 32): 0x29,
    (64, 64): 0x29,
}

RM = {
    (8, 8): 0x2A,
    (16, 16): 0x2B,
    (32, 32): 0x2B,
    (64, 64): 0x2B,
}


def encode_sub_reg_imm(instruction: SUB, bytecode: bytearray) -> None:
    # assume no immediate value for now
    immediate: Optional[Immediate] = None

    # reg/rm will be determined
    reg: kind.RegisterOrConstant
    rm: Optional[kind.RegisterOrAddress] = None

    # handle immediates first
    if isinstance(instruction.src, Immediate):
        immediate = instruction.src
        imm_width = immediate.width

        if isinstance(instruction.dst, Register):
            rm_width = instruction.dst.get_width()
            is_acc = instruction.dst.is_acc()
            reg = instruction.dst
        else:
            rm_width = instruction.dst.width
            is_acc = False
            reg = 0x05

        if is_acc and immediate.width == rm_width and imm_width == 8:
            opcode = 0x2C

        elif is_acc and immediate.width == rm_width and imm_width in (16, 32):
            opcode = 0x2D

        elif is_acc and immediate.width == 32 and rm_width == 64:
            opcode = 0x2D

        else:

            reg, rm = 0x05, instruction.dst
            opcode = MI[rm_width, imm_width]

    elif isinstance(instruction.src, Register):
        reg = instruction.src

        if isinstance(instruction.dst, Register):
            rm_width = instruction.dst.get_width()
        else:
            rm_width = instruction.dst.width

        rm = instruction.dst
        opcode = MR[rm_width, int(reg.width)]

    else:

        assert isinstance(instruction.dst, Register)
        assert isinstance(instruction.src, Address)

        rm = instruction.src
        rm_width = instruction.dst.get_width()

        reg = instruction.dst
        opcode = RM[rm_width, rm_width]

    if rm is None:

        # satisfy type checker
        assert isinstance(reg, Register)

        # derive prefixes and rex
        prefixes = kind.encode_prefixes(reg)
        rex = kind.encode_rex(reg)

        # encode instruction
        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, opcode)
        kind.write_immediate(bytecode, immediate, condition=immediate is not None)

    else:

        # compute ModRM fields
        modrm_reg = kind.encode_modrm_reg(reg)
        modrm_rm = kind.encode_modrm_rm(rm)

        # derive prefixes and rex
        prefixes = kind.encode_prefixes(rm)
        rex = kind.encode_rex(rm, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

        # encode instruction
        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, opcode)
        kind.write_modrm(bytecode, modrm_reg, modrm_rm)
        kind.write_immediate(bytecode, immediate, condition=immediate is not None)


def encode_add_reg_imm(instruction: AddRegImm, bytecode: bytearray):
    pass


def encode_add_reg_reg(instruction: AddRegReg, bytecode: bytearray):

    pass
