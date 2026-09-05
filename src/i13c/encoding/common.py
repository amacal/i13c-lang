from collections.abc import Callable

from i13c.encoding.kind import AddressInfo, RegisterInfo
from i13c.semantic.typing.analyses.llvm import Address, Register


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
SpecType = dict[tuple[int, int], Transform]

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


def encode_rm(
    base: int,
    dst: Register | Address,
    src: Register | Address,
) -> tuple[int, Register | Address, Register]:
    # register to register or memory
    if isinstance(src, Register):
        reg = src
        rm = dst

        if isinstance(dst, Register):
            rm_width = RegisterInfo.get_width(dst)
        else:
            rm_width = AddressInfo.get_width(dst)

        opcode = SPEC["MR"][(rm_width, rm_width)](base)

    # memory to register
    else:
        assert isinstance(dst, Register)
        assert isinstance(src, Address)

        rm = src
        reg = dst

        rm_width = RegisterInfo.get_width(dst)
        opcode = SPEC["RM"][(rm_width, rm_width)](base)

    return (opcode, rm, reg)
