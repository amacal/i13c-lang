from i13c import ast, lex, par, res, sem, src


def can_accept_operands_arity_of_syscall():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.Function(
                    name=b"main",
                    instructions=[
                        ast.Instruction(
                            ref=ast.Reference(offset=0, length=7),
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
                    name=b"main",
                    instructions=[
                        ast.Instruction(
                            ref=ast.Reference(offset=0, length=3),
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
                    name=b"main",
                    instructions=[
                        ast.Instruction(
                            ref=ast.Reference(offset=0, length=3),
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
                    name=b"main",
                    instructions=[
                        ast.Instruction(
                            ref=ast.Reference(offset=0, length=3),
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
                    name=b"main",
                    instructions=[
                        ast.Instruction(
                            ref=ast.Reference(offset=0, length=3),
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
