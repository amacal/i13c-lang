from i13c import ast, err, sem, src


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
