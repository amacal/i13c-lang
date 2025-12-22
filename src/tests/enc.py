from typing import List

from i13c import enc, ir


def can_encode_instructions_mov_rax_imm():
    unit = ir.Unit(
        symbols=set(),
        codeblocks=[
            ir.CodeBlock(
                label=b"main",
                instructions=[
                    ir.MovRegImm(dst=0, imm=0x1234),
                ],
            )
        ],
    )

    bytecode = enc.encode(unit)
    expected = bytes([0x48, 0xB8, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_mov_r10_imm():
    unit = ir.Unit(
        symbols=set(),
        codeblocks=[
            ir.CodeBlock(
                label=b"main",
                instructions=[
                    ir.MovRegImm(dst=10, imm=0x1234),
                ],
            )
        ],
    )

    bytecode = enc.encode(unit)
    expected = bytes([0x49, 0xBA, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    assert bytecode == expected


def can_encode_instructions_syscall():
    unit = ir.Unit(
        symbols=set(),
        codeblocks=[
            ir.CodeBlock(
                label=b"main",
                instructions=[
                    ir.SysCall(),
                ],
            )
        ],
    )

    bytecode = enc.encode(unit)
    expected = bytes([0x0F, 0x05])

    assert bytecode == expected
