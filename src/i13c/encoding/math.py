from typing import Callable

from i13c.encoding import kind
from i13c.encoding.kind import AddressInfo, RegisterInfo
from i13c.semantic.typing.analyses.llvm import (
    ADC,
    ADD,
    AND,
    CMP,
    OR,
    SBB,
    SUB,
    XOR,
    Group1Instruction,
    Address,
    Immediate,
    Register,
)


def div8(value: int) -> int:
    return value // 8


def add0(value: int) -> int:
    return value + 0


def add1(value: int) -> int:
    return value + 1


def add2(value: int) -> int:
    return value + 2


def add3(value: int) -> int:
    return value + 3


def add4(value: int) -> int:
    return value + 4


def add5(value: int) -> int:
    return value + 5


Transform = Callable[[int], int]
ImmType = dict[str, Transform]
SizeType = dict[tuple[int, int], int]
SpecType = dict[tuple[int, int], Transform]


IMM: ImmType = {
    "EXT": div8,
    "AC8": add4,
    "A32": add5,
    "ARM": add5,
}

SIZE: SizeType = {
    (8, 8): 0x80,
    (16, 16): 0x81,
    (32, 32): 0x81,
    (64, 32): 0x81,
    (16, 8): 0x83,
    (32, 8): 0x83,
    (64, 8): 0x83,
}

SPEC: dict[str, SpecType] = {
    "MR": {
        (8, 8): add0,
        (16, 16): add1,
        (32, 32): add1,
        (64, 64): add1,
    },
    "RM": {
        (8, 8): add2,
        (16, 16): add3,
        (32, 32): add3,
        (64, 64): add3,
    },
}


def encode_adc(instruction: ADC, bytecode: bytearray) -> None:
    return encode_group(0x10, instruction, bytecode)


def encode_add(instruction: ADD, bytecode: bytearray) -> None:
    return encode_group(0x00, instruction, bytecode)


def encode_and(instruction: AND, bytecode: bytearray) -> None:
    return encode_group(0x20, instruction, bytecode)


def encode_cmp(instruction: CMP, bytecode: bytearray) -> None:
    return encode_group(0x38, instruction, bytecode)


def encode_or(instruction: OR, bytecode: bytearray) -> None:
    return encode_group(0x08, instruction, bytecode)


def encode_sbb(instruction: SBB, bytecode: bytearray) -> None:
    return encode_group(0x18, instruction, bytecode)


def encode_sub(instruction: SUB, bytecode: bytearray) -> None:
    return encode_group(0x28, instruction, bytecode)


def encode_xor(instruction: XOR, bytecode: bytearray) -> None:
    return encode_group(0x30, instruction, bytecode)


def encode_group(
    base: int, instruction: Group1Instruction, bytecode: bytearray
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
            reg = IMM["EXT"](base)

        # if the dst is the accumulator with imm8
        if is_acc and imm_width == rm_width and imm_width == 8:
            opcode = IMM["AC8"](base)

        # if the dst is the accumulator with imm16/32
        elif is_acc and imm_width == rm_width and imm_width in (16, 32):
            opcode = IMM["A32"](base)

        # if the dst is the accumulator with rm64
        elif is_acc and imm_width == 32 and rm_width == 64:
            opcode = IMM["ARM"](base)

        # default to group 1 opcode
        else:
            reg, rm = IMM["EXT"](base), dst
            opcode = SIZE[(rm_width, imm_width)]

    elif isinstance(src, Register):
        reg = src

        if isinstance(dst, Register):
            rm_width = RegisterInfo.get_width(dst)
        else:
            rm_width = AddressInfo.get_width(dst)

        rm = dst
        opcode = SPEC["MR"][(rm_width, rm_width)](base)

    else:

        assert isinstance(dst, Register)
        assert isinstance(src, Address)

        rm = src
        rm_width = RegisterInfo.get_width(dst)

        reg = dst
        opcode = SPEC["RM"][(rm_width, rm_width)](base)

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
