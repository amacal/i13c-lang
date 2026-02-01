from typing import List

from i13c import encoding as enc
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import (
    Instruction,
    Label,
    MovRegImm,
    ShlRegImm,
    SysCall,
)


def can_encode_instructions_mov_rax_imm():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        MovRegImm(dst=0, imm=0x1234),
    ]

    bytecode = enc.encode(flow)
    expected = bytes([0x48, 0xB8, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_mov_r10_imm():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        MovRegImm(dst=10, imm=0x1234),
    ]

    bytecode = enc.encode(flow)
    expected = bytes([0x49, 0xBA, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_shl_rbx_imm():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        ShlRegImm(dst=3, imm=0x01),
    ]

    bytecode = enc.encode(flow)
    expected = bytes([0x48, 0xC1, 0xE3, 0x01])

    assert bytecode == expected


def can_encode_instructions_syscall():
    flow: List[Instruction] = [
        Label(id=BlockId(value=0)),
        SysCall(),
    ]

    bytecode = enc.encode(flow)
    expected = bytes([0x0F, 0x05])

    assert bytecode == expected
