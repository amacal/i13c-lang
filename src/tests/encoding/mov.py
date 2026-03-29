from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction, Label, MovRegImm


def can_encode_instructions_mov_rax_imm():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        MovRegImm(dst=0, imm=0x1234),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0xB8, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_mov_r10_imm():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        MovRegImm(dst=10, imm=0x1234),
    ]

    bytecode = encode(flow)
    expected = bytes([0x49, 0xBA, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected
