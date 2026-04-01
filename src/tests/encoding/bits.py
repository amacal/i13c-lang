from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.bits import ByteSwapReg32, ByteSwapReg64, ShlRegImm


def can_encode_instructions_bswap_eax():
    flow: List[Instruction] = [
        ByteSwapReg32(target=0),
    ]

    bytecode = encode(flow)
    expected = bytes([0x0F, 0xC8])

    assert bytecode == expected


def can_encode_instructions_bswap_rax():
    flow: List[Instruction] = [
        ByteSwapReg64(target=0),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0x0F, 0xC8])

    assert bytecode == expected


def can_encode_instructions_shl_rbx_imm():
    flow: List[Instruction] = [
        ShlRegImm(dst=3, imm=0x01),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0xC1, 0xE3, 0x01])

    assert bytecode == expected
