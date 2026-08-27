from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo, RelocationTarget
from i13c.encoding.kind import ImmediateInfo, RegisterInfo
from i13c.semantic.typing.analyses.llvm import (
    MOV,
    XCHG,
    Address,
    Fixed,
    Immediate,
    Register,
)


def encode_mov(instruction: MOV, bytecode: bytearray) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume optional encoding components
    immediate: Immediate | None = None
    opcode_reg: kind.OpCodeEncoding | None = None
    reg: kind.RegisterOrConstant | None = None
    rm: kind.RegisterOrAddress | None = None

    # optionally created relocation info
    relocation: RelocationInfo | None = None
    target: RelocationTarget | None = None

    # mov reg, imm
    if isinstance(dst, Register) and isinstance(src, Immediate):
        width = RegisterInfo.get_width(dst)

        if width == 64 and ImmediateInfo.fits_signed(src, 32):
            opcode = 0xc7
            reg = 0x00
            rm = dst
            immediate = ImmediateInfo.normalize(src, 32)

        else:
            opcode = 0xB0 if width == 8 else 0xB8
            opcode_reg = kind.encode_opcode_reg(dst)
            immediate = ImmediateInfo.normalize(src, width)

    # mov r/m, imm
    elif isinstance(src, Immediate):
        opcode = 0xC7
        reg = 0x00
        rm = dst
        immediate = ImmediateInfo.normalize(src, 32)

    # mov r/m, reg
    elif isinstance(src, Register):
        width = RegisterInfo.get_width(src)
        opcode = 0x88 if width == 8 else 0x89

        reg = src
        rm = dst

    # mov reg, r/m
    else:
        assert isinstance(dst, Register)
        assert isinstance(src, (Address, Fixed))

        opcode = 0x8B
        reg = dst
        rm = src

    # encode opcode-register form
    if opcode_reg is not None:
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

    # encode ModRM form
    else:
        assert reg is not None
        assert rm is not None

        if isinstance(reg, Register):
            rex_rm = reg
        else:
            rex_rm = rm

        modrm_reg = kind.encode_modrm_reg(reg)
        modrm_rm = kind.encode_modrm_rm(rm)

        prefixes = kind.encode_prefixes(rm)
        rex = kind.encode_rex(rex_rm, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, opcode)
        kind.write_modrm(bytecode, modrm_reg, modrm_rm)

        # the address may require relocation
        if target is not None:
            relocation = RelocationInfo(
                target=target,
                offset=len(bytecode),
                width=4,
            )

    # encode optional immediate
    kind.write_immediate(bytecode, immediate)

    return relocation


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
