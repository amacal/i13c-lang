from i13c import ast, err, sem, src


def can_detect_reg_integer_literal_out_of_range():
    diagnostics = sem.e3007.validate_integer_literal_out_of_range(
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
