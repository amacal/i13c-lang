from i13c import ast, err, ir, low, res, src


def can_lower_syscall_program():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                terminal=False,
                parameters=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=10, length=6),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    ),
                ],
            )
        ]
    )

    unit = low.lower(program)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry == 0

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1
    assert isinstance(instructions[0], ir.SysCall)


def can_lower_mov_program():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                terminal=False,
                parameters=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=10, length=10),
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
    assert unit.value.entry == 0

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1

    instruction = instructions[0]
    assert isinstance(instruction, ir.MovRegImm)

    assert instruction.dst == 0
    assert instruction.imm == 0x1234


def can_lower_noentry_program():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=0, length=4),
                name=b"aux",
                terminal=False,
                parameters=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=10, length=6),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    ),
                ],
            )
        ]
    )

    unit = low.lower(program)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry is None

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1
    assert isinstance(instructions[0], ir.SysCall)


def can_detect_unsupported_mnemonic():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                terminal=False,
                parameters=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=10, length=4),
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

    assert diagnostics[0].code == err.ERROR_4000
    assert diagnostics[0].ref.offset == 10
    assert diagnostics[0].ref.length == 4
