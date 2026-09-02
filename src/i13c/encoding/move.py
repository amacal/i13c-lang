from i13c.encoding import kind
from i13c.encoding.kind import AddressInfo, ImmediateInfo, RegisterInfo
from i13c.encoding.math import encode_mr
from i13c.semantic.typing.analyses.llvm import MOV, XCHG, Immediate, Register

MOV_MEM_IMM: dict[tuple[int, int], int] = {
    (8, 8): 0xc6,
    (16, 16): 0xc7,
    (32, 32): 0xc7,
    (64, 32): 0xc7,
}

MOV_REG_IMM: dict[tuple[int, int], int] = {
    (8, 8): 0xb0,
    (16, 16): 0xb8,
    (32, 32): 0xb8,
    (64, 64): 0xb8,
}


def encode_mov(instruction: MOV, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume optional encoding components
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
        opcode, rm, reg = encode_mr(0x88, dst, src)

    if immediate is not None and opcode_reg is not None:
        prefixes = kind.encode_prefixes(dst)
        rex = kind.encode_rex(dst, opcode_reg=opcode_reg)

        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)

        kind.write_opcode(
            bytecode,
            1,
            opcode,
            opcode_reg=opcode_reg,
        )

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

    # encode optional immediate
    kind.write_immediate(bytecode, immediate)


def encode_xchg(instruction: XCHG, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    reg = src
    rm = dst

    width = RegisterInfo.get_width(src)
    opcode = 0x86 if width == 8 else 0x87

    modrm_reg = kind.encode_modrm_reg(reg)
    modrm_rm = kind.encode_modrm_rm(rm)

    prefixes = kind.encode_prefixes(rm)
    rex = kind.encode_rex(
        rm,
        modrm_reg=modrm_reg,
        modrm_rm=modrm_rm,
    )

    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, opcode)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)
