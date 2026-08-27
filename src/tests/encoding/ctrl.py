from i13c.encoding import encode
from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.analyses.blocklets import Blocklet, BlockletBlock, BlockletId
from i13c.semantic.typing.analyses.llvm import JMP, NOP, Relocation
from i13c.syntax.source import Span


def can_encode_instructions_nop_twice():
    blocklet = Blocklet(
        ref=Span(offset=0, length=3),
        id=BlockletId(value=1),
        target=AsmletId(value=2),
        blocks=[
            BlockletBlock(
                instructions=[
                    NOP(),
                    NOP(),
                ]
            )
        ],
    )

    bytecode = encode([blocklet])
    expected = bytes([0x90, 0x90])

    assert bytecode == expected


def can_encode_instructions_jump_forward():
    blocklet = Blocklet(
        ref=Span(offset=0, length=3),
        id=BlockletId(value=1),
        target=AsmletId(value=2),
        blocks=[
            BlockletBlock(
                instructions=[
                    JMP(operands=(Relocation(block=1),)),
                    NOP(),
                ]
            ),
            BlockletBlock(
                instructions=[
                    NOP(),
                ]
            ),
        ],
    )

    bytecode = encode([blocklet])
    expected = bytes(
        [
            0xE9,  # JMP +1
            0x01,
            0x00,
            0x00,
            0x00,
            0x90,  # NOP in block 0
            0x90,  # NOP in block 1
        ]
    )

    assert bytecode == expected


def can_encode_instructions_jump_backward():
    blocklet = Blocklet(
        ref=Span(offset=0, length=3),
        id=BlockletId(value=1),
        target=AsmletId(value=2),
        blocks=[
            BlockletBlock(
                instructions=[
                    NOP(),
                ]
            ),
            BlockletBlock(
                instructions=[
                    JMP(operands=(Relocation(block=0),)),
                    NOP(),
                ]
            ),
        ],
    )

    bytecode = encode([blocklet])
    expected = bytes(
        [
            0x90,  # NOP in block 0
            0xE9,  # JMP -6
            0xFA,
            0xFF,
            0xFF,
            0xFF,
            0x90,  # NOP in block 1
        ]
    )

    assert bytecode == expected
