from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import AddRegImm, AddRegReg, Instruction, Label


def can_encode_instructions_add_rbx_imm32():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        AddRegImm(dst=3, imm=0x12345678),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0x81, 0xC3, 0x78, 0x56, 0x34, 0x12])

    assert bytecode == expected


def can_encode_instructions_add_r15_rbx():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        AddRegReg(dst=15, src=3),
    ]

    bytecode = encode(flow)
    expected = bytes([0x49, 0x01, 0xDF])

    assert bytecode == expected
