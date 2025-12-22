from i13c import ast, lex, par, res, sem, src


def can_accept_operands_arity_of_syscall():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=7),
                            mnemonic=ast.Mnemonic(name=b"syscall"),
                            operands=[],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 0


def can_accept_operands_arity_of_mov():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=3),
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


def can_detect_invalid_instruction():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=3),
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

    assert diagnostic.offset == 0
    assert diagnostic.code == "V001"


def can_detect_immediate_out_of_range():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=3),
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

    assert diagnostic.offset == 0
    assert diagnostic.code == "V002"


def can_detect_invalid_operand_types_of_mov():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=3),
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

    assert diagnostic.offset == 0
    assert diagnostic.code == "V003"


def can_detect_duplicated_parameter_bindings():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[
                        ast.Parameter(
                            name=b"code",
                            type=ast.Type(name=b"u32"),
                            bind=ast.Register(name=b"rdi"),
                        ),
                        ast.Parameter(
                            name=b"id",
                            type=ast.Type(name=b"u16"),
                            bind=ast.Register(name=b"rdi"),
                        ),
                    ],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=3),
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

    assert diagnostic.offset == 0
    assert diagnostic.code == "V004"


def can_detect_duplicated_parameter_names():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
                    name=b"main",
                    terminal=False,
                    parameters=[
                        ast.Parameter(
                            name=b"code",
                            type=ast.Type(name=b"u32"),
                            bind=ast.Register(name=b"rdi"),
                        ),
                        ast.Parameter(
                            name=b"code",
                            type=ast.Type(name=b"u16"),
                            bind=ast.Register(name=b"rax"),
                        ),
                    ],
                    clobbers=[],
                    instructions=[
                        ast.Instruction(
                            ref=ast.Span(offset=0, length=3),
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

    assert diagnostic.offset == 0
    assert diagnostic.code == "V005"


def can_detect_duplicated_clobbers():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    ref=ast.Span(offset=0, length=4),
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
                            ref=ast.Span(offset=0, length=3),
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

    assert diagnostic.offset == 0
    assert diagnostic.code == "V006"
