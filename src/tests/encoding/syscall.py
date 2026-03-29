from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction, Label, SysCall


def can_encode_instructions_syscall():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        SysCall(),
    ]

    bytecode = encode(flow)
    expected = bytes([0x0F, 0x05])

    assert bytecode == expected
