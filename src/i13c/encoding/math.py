from i13c.encoding import kind
from i13c.encoding.kind import AddressInfo, RegisterInfo
from i13c.semantic.typing.analyses.llvm import (
    ADD,
    AND,
    OR,
    SUB,
    Address,
    Immediate,
    Register,
)

ImmType = dict[str, int]
OpsType = dict[str, dict[tuple[int, int], int]]

IMM: dict[str, ImmType] = {
    "ADD": {
        "EXT": 0x00,
        "AC8": 0x04,
        "A32": 0x05,
        "ARM": 0x05,
    },
    "AND": {
        "EXT": 0x04,
        "AC8": 0x24,
        "A32": 0x25,
        "ARM": 0x25,
    },
    "OR": {
        "EXT": 0x01,
        "AC8": 0x0C,
        "A32": 0x0D,
        "ARM": 0x0D,
    },
    "SUB": {
        "EXT": 0x05,
        "AC8": 0x2C,
        "A32": 0x2D,
        "ARM": 0x2D,
    },
}


OPS: dict[str, OpsType] = {
    "ADD": {
        "MI": {
            (8, 8): 0x80,
            (16, 16): 0x81,
            (32, 32): 0x81,
            (64, 32): 0x81,
            (16, 8): 0x83,
            (32, 8): 0x83,
            (64, 8): 0x83,
        },
        "MR": {
            (8, 8): 0x00,
            (16, 16): 0x01,
            (32, 32): 0x01,
            (64, 64): 0x01,
        },
        "RM": {
            (8, 8): 0x02,
            (16, 16): 0x03,
            (32, 32): 0x03,
            (64, 64): 0x03,
        },
    },
    "AND": {
        "MI": {
            (8, 8): 0x80,
            (16, 16): 0x81,
            (32, 32): 0x81,
            (64, 32): 0x81,
            (16, 8): 0x83,
            (32, 8): 0x83,
            (64, 8): 0x83,
        },
        "MR": {
            (8, 8): 0x20,
            (16, 16): 0x21,
            (32, 32): 0x21,
            (64, 64): 0x21,
        },
        "RM": {
            (8, 8): 0x22,
            (16, 16): 0x23,
            (32, 32): 0x23,
            (64, 64): 0x23,
        },
    },
    "OR": {
        "MI": {
            (8, 8): 0x80,
            (16, 16): 0x81,
            (32, 32): 0x81,
            (64, 32): 0x81,
            (16, 8): 0x83,
            (32, 8): 0x83,
            (64, 8): 0x83,
        },
        "MR": {
            (8, 8): 0x08,
            (16, 16): 0x09,
            (32, 32): 0x09,
            (64, 64): 0x09,
        },
        "RM": {
            (8, 8): 0x0A,
            (16, 16): 0x0B,
            (32, 32): 0x0B,
            (64, 64): 0x0B,
        },
    },
    "SUB": {
        "MI": {
            (8, 8): 0x80,
            (16, 16): 0x81,
            (32, 32): 0x81,
            (64, 32): 0x81,
            (16, 8): 0x83,
            (32, 8): 0x83,
            (64, 8): 0x83,
        },
        "MR": {
            (8, 8): 0x28,
            (16, 16): 0x29,
            (32, 32): 0x29,
            (64, 64): 0x29,
        },
        "RM": {
            (8, 8): 0x2A,
            (16, 16): 0x2B,
            (32, 32): 0x2B,
            (64, 64): 0x2B,
        },
    },
}


def encode_add(instruction: ADD, bytecode: bytearray) -> None:
    return encode_group(IMM["ADD"], OPS["ADD"], instruction, bytecode)


def encode_and(instruction: AND, bytecode: bytearray) -> None:
    return encode_group(IMM["AND"], OPS["AND"], instruction, bytecode)


def encode_or(instruction: OR, bytecode: bytearray) -> None:
    return encode_group(IMM["OR"], OPS["OR"], instruction, bytecode)


def encode_sub(instruction: SUB, bytecode: bytearray) -> None:
    return encode_group(IMM["SUB"], OPS["SUB"], instruction, bytecode)


def encode_group(
    imm: ImmType, ops: OpsType, instruction: ADD | AND | OR | SUB, bytecode: bytearray
) -> None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume no immediate value for now
    immediate: Immediate | None = None

    # reg/rm will be determined
    reg: kind.RegisterOrConstant
    rm: kind.RegisterOrAddress | None = None

    # handle immediates first
    if isinstance(src, Immediate):
        immediate = src
        imm_width = immediate.width()

        if isinstance(dst, Register):
            rm_width = RegisterInfo.get_width(dst)
            is_acc = RegisterInfo.is_acc(dst)
            reg = dst

        # if the dst is an address
        else:
            rm_width = AddressInfo.get_width(dst)
            is_acc = False
            reg = imm["EXT"]

        # if the dst is the accumulator with imm8
        if is_acc and imm_width == rm_width and imm_width == 8:
            opcode = imm["AC8"]

        # if the dst is the accumulator with imm16/32
        elif is_acc and imm_width == rm_width and imm_width in (16, 32):
            opcode = imm["A32"]

        # if the dst is the accumulator with rm64
        elif is_acc and imm_width == 32 and rm_width == 64:
            opcode = imm["ARM"]

        # default to group 1 opcode
        else:
            reg, rm = imm["EXT"], dst
            opcode = ops["MI"][(rm_width, imm_width)]

    elif isinstance(src, Register):
        reg = src

        if isinstance(dst, Register):
            rm_width = RegisterInfo.get_width(dst)
        else:
            rm_width = AddressInfo.get_width(dst)

        rm = dst
        opcode = ops["MR"][(rm_width, RegisterInfo.get_width(reg))]

    else:

        assert isinstance(dst, Register)
        assert isinstance(src, Address)

        rm = src
        rm_width = RegisterInfo.get_width(dst)

        reg = dst
        opcode = ops["RM"][(rm_width, rm_width)]

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
