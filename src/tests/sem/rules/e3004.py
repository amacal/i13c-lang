from i13c import ast, err, sem, src
from i13c.sem import build


def can_detect_duplicated_asm_parameter_names():
    program = ast.Program(
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

    relationships = build.build_semantic(program)
    diagnostics = sem.e3004.validate_duplicated_parameter_names(relationships)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


def can_detect_duplicated_reg_parameter_names():
    program = ast.Program(
        functions=[
            ast.RegFunction(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                terminal=False,
                parameters=[
                    ast.RegParameter(
                        name=b"code",
                        type=ast.Type(name=b"u32"),
                    ),
                    ast.RegParameter(
                        name=b"code",
                        type=ast.Type(name=b"u16"),
                    ),
                ],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=22, length=6),
                        name=b"foo",
                        arguments=[],
                    )
                ],
            )
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3004.validate_duplicated_parameter_names(relationships)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20
