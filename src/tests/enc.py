from typing import List
from i13c import ir, enc


def can_encode_instructions_mov_rax_imm():
    codeblocks: List[ir.CodeBlock] = [
        ir.CodeBlock(
            instructions=[
                ir.MovRegImm(dst=0, imm=0x1234),
            ]
        )
    ]

    bytecode = enc.encode(codeblocks)
    expected = bytes([0x48, 0xB8, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_mov_r10_imm():
    codeblocks: List[ir.CodeBlock] = [
        ir.CodeBlock(
            instructions=[
                ir.MovRegImm(dst=10, imm=0x1234),
            ]
        )
    ]

    bytecode = enc.encode(codeblocks)
    expected = bytes([0x49, 0xBA, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_syscall():
    codeblocks: List[ir.CodeBlock] = [
        ir.CodeBlock(
            instructions=[
                ir.SysCall(),
            ]
        )
    ]

    bytecode = enc.encode(codeblocks)
    expected = bytes([0x0F, 0x05])

    assert bytecode == expected
