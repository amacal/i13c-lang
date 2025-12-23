from i13c import ast, err, sem, src


def can_detect_duplicated_reg_parameter_names():
    diagnostics = sem.validate(
        ast.Program(
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
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


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


def can_detect_reg_integer_literal_out_of_range():
    diagnostics = sem.validate(
        ast.Program(
            functions=[
                ast.RegFunction(
                    ref=src.Span(offset=1, length=20),
                    name=b"main",
                    terminal=False,
                    parameters=[],
                    statements=[
                        ast.CallStatement(
                            ref=src.Span(offset=12, length=20),
                            name=b"foo",
                            arguments=[ast.IntegerLiteral(value=0x1FFFFFFFFFFFFFFFF)],
                        )
                    ],
                )
            ]
        )
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
