from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import ByteSwap, Instruction, Label


def can_encode_instructions_bswap_rax():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        ByteSwap(target=0),
    ]

    bytecode = encode(flow)
    expected = bytes([0x48, 0x0F, 0xC8])

    assert bytecode == expected
