from i13c import ast, err, sem, src


def can_detect_duplicated_asm_parameter_bindings():
    diagnostics = sem.e3003.validate_duplicated_parameter_bindings(
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
