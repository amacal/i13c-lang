from i13c import ast, err, sem, src
from i13c.sem import build


def can_detect_missing_called_symbol():
    program = ast.Program(
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
                        arguments=[],
                    )
                ],
            )
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3008.validate_called_symbol_exists(relationships)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3008
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
