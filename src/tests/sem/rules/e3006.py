from i13c import ast, err, sem, src


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


def can_detect_duplicated_reg_function_names():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.RegFunction(
                    ref=src.Span(offset=1, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    statements=[
                        ast.CallStatement(
                            ref=src.Span(offset=12, length=6),
                            name=b"foo",
                            arguments=[],
                        )
                    ],
                ),
                ast.RegFunction(
                    ref=src.Span(offset=20, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    statements=[
                        ast.CallStatement(
                            ref=src.Span(offset=32, length=6),
                            name=b"bar",
                            arguments=[],
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


def can_detect_duplicated_mixed_function_names():
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
                ast.RegFunction(
                    ref=src.Span(offset=20, length=10),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    statements=[
                        ast.CallStatement(
                            ref=src.Span(offset=32, length=6),
                            name=b"bar",
                            arguments=[],
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
