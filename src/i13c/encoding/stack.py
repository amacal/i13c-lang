from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo
from i13c.semantic.typing.analyses.llvm import (
    POP,
    PUSH,
    Immediate,
    Register,
    Relocation,
)


def encode_push(instruction: PUSH, bytecode: bytearray) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # optional relocation
    relocation: RelocationInfo | None = None

    # handle immediates
    if isinstance(target, Immediate):
        match target.width():
            case 8:
                opcode = 0x6A
                prefixes = kind.PrefixEncoding.default()
            case 16:
                opcode = 0x68
                prefixes = kind.encode_prefixes(target)
            case 32:
                opcode = 0x68
                prefixes = kind.PrefixEncoding.default()
            case _:
                assert False

        kind.write_prefixes(bytecode, prefixes)
        kind.write_opcode(bytecode, 1, opcode)
        kind.write_immediate(bytecode, target)

    # handle shorter form opcode for registers
    elif isinstance(target, Register):
        opcode_reg = kind.encode_opcode_reg(target, mode="64-bit")
        prefixes = kind.encode_prefixes(target)
        rex = kind.encode_rex(None, opcode_reg=opcode_reg)

        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, 0x50, opcode_reg)

    # memory operands go through ModRM
    else:
        # compute ModRM fields
        modrm_reg = kind.encode_modrm_reg(0x06)
        modrm_rm = kind.encode_modrm_rm(target)

        # derive prefixes and rex
        prefixes = kind.encode_prefixes(target)
        rex = kind.encode_rex(
            target,
            modrm_reg=modrm_reg,
            modrm_rm=modrm_rm,
        )

        # encode instruction
        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, 0xFF)
        kind.write_modrm(bytecode, modrm_reg, modrm_rm)

        # check if the r/m operand has a relocation displacement
        if isinstance(target.disp, Relocation):
            relocation = RelocationInfo(
                target=target.disp.block,
                offset=len(bytecode) - 4,
                width=4,
            )

    # optional relocation
    return relocation


def encode_pop(instruction: POP, bytecode: bytearray) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # optional relocation
    relocation: RelocationInfo | None = None

    # handle shorter form opcode for registers
    if isinstance(target, Register):
        opcode_reg = kind.encode_opcode_reg(target, mode="64-bit")
        prefixes = kind.encode_prefixes(target)
        rex = kind.encode_rex(None, opcode_reg=opcode_reg)

        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, 0x58, opcode_reg)

    # memory operands go through ModRM
    else:
        # compute ModRM fields
        modrm_reg = kind.encode_modrm_reg(0x00)
        modrm_rm = kind.encode_modrm_rm(target)

        # derive prefixes and rex
        prefixes = kind.encode_prefixes(target)
        rex = kind.encode_rex(
            target,
            modrm_reg=modrm_reg,
            modrm_rm=modrm_rm,
        )

        # encode instruction
        kind.write_prefixes(bytecode, prefixes)
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, 0x8F)
        kind.write_modrm(bytecode, modrm_reg, modrm_rm)

        # check if the r/m operand has a relocation displacement
        if isinstance(target.disp, Relocation):
            relocation = RelocationInfo(
                target=target.disp.block,
                offset=len(bytecode) - 4,
                width=4,
            )

    # optional relocation
    return relocation
