from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction, Nop


def can_encode_instructions_nop_twice():
    flow: List[Instruction] = [
        Nop(),
        Nop(),
    ]

    bytecode = encode(flow)
    expected = bytes([0x90, 0x90])

    assert bytecode == expected
