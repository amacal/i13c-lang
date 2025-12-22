import pytest

from i13c import ast, ir, low, res


def can_lower_syscall_program():
    program = ast.Program(
        functions=[
            ast.Function(
                name=b"main",
                instructions=[
                    ast.Instruction(
                        ref=ast.Reference(offset=0, length=7),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    ),
                ],
            )
        ]
    )

    unit = low.lower(program)
    assert isinstance(unit, res.Ok)

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1
    assert isinstance(instructions[0], ir.SysCall)


def can_lower_mov_program():
    program = ast.Program(
        functions=[
            ast.Function(
                name=b"main",
                instructions=[
                    ast.Instruction(
                        ref=ast.Reference(offset=0, length=3),
                        mnemonic=ast.Mnemonic(name=b"mov"),
                        operands=[
                            ast.Register(name=b"rax"),
                            ast.Immediate(value=0x1234),
                        ],
                    ),
                ],
            )
        ]
    )

    unit = low.lower(program)
    assert isinstance(unit, res.Ok)

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1

    instruction = instructions[0]
    assert isinstance(instruction, ir.MovRegImm)

    assert instruction.dst == 0
    assert instruction.imm == 0x1234


def can_detect_unknown_mnemonic():
    program = ast.Program(
        functions=[
            ast.Function(
                name=b"main",
                instructions=[
                    ast.Instruction(
                        ref=ast.Reference(offset=0, length=4),
                        mnemonic=ast.Mnemonic(name=b"abcd"),
                        operands=[],
                    ),
                ],
            )
        ]
    )

    codeblocks = low.lower(program)
    assert isinstance(codeblocks, res.Err)

    diagnostics = codeblocks.error
    assert len(diagnostics) == 1

    assert diagnostics[0].code == "V001"
