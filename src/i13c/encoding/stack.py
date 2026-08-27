from i13c.encoding import kind
from i13c.semantic.typing.analyses.llvm import POP, PUSH


def encode_push(instruction: PUSH, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

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


def encode_pop(instruction: POP, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

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
