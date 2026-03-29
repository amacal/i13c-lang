from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction, Label, ShlRegImm


def can_encode_instructions_shl_rbx_imm():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        ShlRegImm(dst=3, imm=0x01),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0xC1, 0xE3, 0x01])

    assert bytecode == expected
