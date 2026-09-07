from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo
from i13c.encoding.kind import AddressInfo, ImmediateInfo, RegisterInfo
from i13c.encoding.math import encode_rm
from i13c.semantic.typing.analyses.llvm import (
    MOV,
    XCHG,
    Immediate,
    Register,
    Address,
    Relocation,
)

MOV_MEM_IMM: dict[tuple[int, int], int] = {
    (8, 8): 0xC6,
    (16, 16): 0xC7,
    (32, 32): 0xC7,
    (64, 32): 0xC7,
}

MOV_REG_IMM: dict[tuple[int, int], int] = {
    (8, 8): 0xB0,
    (16, 16): 0xB8,
    (32, 32): 0xB8,
    (64, 64): 0xB8,
}


def encode_mov(instruction: MOV, bytecode: bytearray) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume optional encoding components
    relocation: RelocationInfo | None = None
    immediate: Immediate | None = None
    opcode: int | None = None
    opcode_reg: kind.OpCodeEncoding | None = None
    reg: kind.RegisterOrConstant | None = None
    rm: kind.RegisterOrAddress | None = None

    if isinstance(src, Immediate):
        immediate = src
        imm_width = ImmediateInfo.get_width(src)

        rm = dst
        reg = 0x00

        # mov reg, imm if widths match
        if isinstance(dst, Register) and RegisterInfo.get_width(dst) == imm_width:
            rm_width = RegisterInfo.get_width(dst)
            opcode = MOV_REG_IMM[(rm_width, imm_width)]
            opcode_reg = kind.encode_opcode_reg(dst)

        elif isinstance(dst, Register):
            rm_width = RegisterInfo.get_width(dst)
            opcode = MOV_MEM_IMM[(rm_width, imm_width)]

        # mov r/m, imm
        else:
            rm_width = AddressInfo.get_width(dst)
            opcode = MOV_MEM_IMM[(rm_width, imm_width)]

    else:
        opcode, rm, reg = encode_rm(0x88, dst, src)

    if immediate is not None and opcode_reg is not None:
        prefixes = kind.encode_prefixes(dst)
        rex = kind.encode_rex(dst, opcode_reg=opcode_reg)

        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, opcode, opcode_reg=opcode_reg)

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

        # check if the r/m operand has a relocation displacement
        if isinstance(rm, Address) and isinstance(rm.disp, Relocation):
            relocation = RelocationInfo(
                target=rm.disp.block,
                offset=len(bytecode) - 4,
                width=4,
            )

    # encode optional immediate
    kind.write_immediate(bytecode, immediate)

    # optional relocation
    return relocation


def encode_xchg(instruction: XCHG, bytecode: bytearray) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume optional encoding components
    relocation: RelocationInfo | None = None
    opcode: int | None = None
    opcode_reg: kind.OpCodeEncoding | None = None
    reg: kind.RegisterOrConstant | None = None
    rm: kind.RegisterOrAddress | None = None

    # try to find shortest form optimization
    if isinstance(dst, Register) and isinstance(src, Register):
        src2, dst2 = src, dst

        if RegisterInfo.is_acc(src2):
            src2, dst2 = dst2, src2

        # only acc but not 8-bit
        if RegisterInfo.is_acc(dst2) and RegisterInfo.get_width(dst2) > 8:
            opcode = 0x90
            opcode_reg = kind.encode_opcode_reg(src2)
            src, dst = src2, dst2

    # move r/m to the left side if necessary
    if isinstance(src, Address) and isinstance(dst, Register):
        src, dst = dst, src

    # if shortest form is available
    if opcode is not None:
        prefixes = kind.encode_prefixes(dst)
        rex = kind.encode_rex(dst, opcode_reg=opcode_reg)

        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, opcode, opcode_reg=opcode_reg)

    # fallback to the longer form
    else:
        # derive standard ModRM encoding for the instruction
        opcode, rm, reg = encode_rm(0x86, dst, src)

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

        # check if the r/m operand has a relocation displacement
        if isinstance(rm, Address) and isinstance(rm.disp, Relocation):
            relocation = RelocationInfo(
                target=rm.disp.block,
                offset=len(bytecode) - 4,
                width=4,
            )

    # optional relocation
    return relocation
