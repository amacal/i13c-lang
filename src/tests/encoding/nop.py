from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction, Jump, Label, Nop


def can_encode_instructions_jump_forward():
    flow: List[Instruction] = [
        Jump(target=BlockId(value=1)),
        Nop(),
        Label(id=BlockId(value=1)),
    ]

    bytecode = encode(flow)
    expected = bytes([0xE9, 0x01, 0x00, 0x00, 0x00, 0x90])

    assert bytecode == expected
