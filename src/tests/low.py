import pytest

from i13c import ast, ir, low


def can_lower_syscall_program():
    program = ast.Program(
        instructions=[
            ast.Instruction(
                ref=ast.Reference(offset=0, length=7),
                mnemonic=ast.Mnemonic(name=b"syscall"),
                operands=[],
            ),
        ]
    )

    instructions = low.lower(program)
    assert len(instructions) == 1

    instruction = instructions[0]
    assert isinstance(instruction, ir.SysCall)


def can_lower_mov_program():
    program = ast.Program(
        instructions=[
            ast.Instruction(
                ref=ast.Reference(offset=0, length=3),
                mnemonic=ast.Mnemonic(name=b"mov"),
                operands=[
                    ast.Register(name=b"rax"),
                    ast.Immediate(value=0x1234),
                ],
            ),
        ]
    )

    instructions = low.lower(program)
    assert len(instructions) == 1

    instruction = instructions[0]
    assert isinstance(instruction, ir.MovRegImm)

    assert instruction.dst == 0
    assert instruction.imm == 0x1234


def can_detect_unknown_mnemonic():
    program = ast.Program(
        instructions=[
            ast.Instruction(
                ref=ast.Reference(offset=0, length=4),
                mnemonic=ast.Mnemonic(name=b"abcd"),
                operands=[],
            ),
        ]
    )

    with pytest.raises(low.UnknownMnemonic) as ex:
        low.lower(program)

    assert ex.value.name == b"abcd"
