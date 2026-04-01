from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.addr import LeaRegOff


def can_encode_instructions_lea_rbx_off():
    flow: List[Instruction] = [
        LeaRegOff(dst=3, src=3, off=0x12345678),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0x8D, 0x9B, 0x78, 0x56, 0x34, 0x12])

    assert bytecode == expected
