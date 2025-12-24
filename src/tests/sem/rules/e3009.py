from i13c import ast, err, sem, src
from i13c.sem import build


def can_detect_non_asm_called_symbol():
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
            ),
            ast.RegFunction(
                ref=src.Span(offset=30, length=10),
                name=b"foo",
                terminal=True,
                parameters=[],
                statements=[],
            ),
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3009.validate_called_symbol_is_asm(relationships)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3009
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
