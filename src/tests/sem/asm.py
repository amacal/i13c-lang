from i13c import ast, err, sem, src


def can_accept_asm_operands_arity_of_syscall():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=0, length=7),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 0


def can_accept_asm_operands_arity_of_mov():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=0, length=3),
                            mnemonic=ast.Mnemonic(name=b"mov"),
                            operands=[
                                ast.Register(name=b"rax"),
                                ast.Immediate(value=0x1234),
                            ],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 0


def can_detect_invalid_asm_instruction():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=12, length=3),
                            mnemonic=ast.Mnemonic(name=b"xyz"),
                            operands=[],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3000
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 3


def can_detect_asm_immediate_out_of_range():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=12, length=20),
                            mnemonic=ast.Mnemonic(name=b"mov"),
                            operands=[
                                ast.Register(name=b"rax"),
                                ast.Immediate(value=0x1_FFFFFFFF_FFFFFFFF),
                            ],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3001
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20


def can_detect_invalid_asm_operand_types_of_mov():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=12, length=15),
                            mnemonic=ast.Mnemonic(name=b"mov"),
                            operands=[
                                ast.Immediate(value=0x1234),
                                ast.Immediate(value=0x5678),
                            ],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3002
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 15


def can_detect_duplicated_asm_parameter_bindings():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=20),
                    name=b"main",
                    terminal=False,
                    parameters=[
                        ast.AsmParameter(
                            name=b"code",
                            type=ast.Type(name=b"u32"),
                            bind=ast.Register(name=b"rdi"),
                        ),
                        ast.AsmParameter(
                            name=b"id",
                            type=ast.Type(name=b"u16"),
                            bind=ast.Register(name=b"rdi"),
                        ),
                    ],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=22, length=6),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3003
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


def can_detect_duplicated_asm_parameter_names():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=20),
                    name=b"main",
                    terminal=False,
                    parameters=[
                        ast.AsmParameter(
                            name=b"code",
                            type=ast.Type(name=b"u32"),
                            bind=ast.Register(name=b"rdi"),
                        ),
                        ast.AsmParameter(
                            name=b"code",
                            type=ast.Type(name=b"u16"),
                            bind=ast.Register(name=b"rax"),
                        ),
                    ],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=22, length=6),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


def can_detect_duplicated_asm_clobbers():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=20),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[
                        ast.Register(name=b"rax"),
                        ast.Register(name=b"rbx"),
                        ast.Register(name=b"rax"),
                    ],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=22, length=6),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


def can_detect_duplicated_asm_function_names():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.AsmFunction(
                    ref=src.Span(offset=1, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=12, length=6),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                ),
                ast.AsmFunction(
                    ref=src.Span(offset=20, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=src.Span(offset=32, length=6),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                ),
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3006
    assert diagnostic.ref.offset == 20
    assert diagnostic.ref.length == 10
