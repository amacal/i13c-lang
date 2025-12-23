from i13c import ast, err, sem, src


def can_accept_asm_operands_arity_of_syscall():
    diagnostics = sem.e3000.validate_assembly_mnemonic(
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
    diagnostics = sem.validate_1st_pass(
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
    diagnostics = sem.validate_1st_pass(
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
