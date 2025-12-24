from i13c import ast, err, sem, src
from i13c.sem import build


def can_survive_non_terminal_callee_symbol():
    program = ast.Program(
        functions=[
            ast.RegFunction(
                ref=src.Span(offset=1, length=20),
                name=b"bar",
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
    diagnostics = sem.e3010.validate_called_symbol_termination(relationships)

    assert len(diagnostics) == 0


def can_detect_non_terminal_caller_symbol():
    program = ast.Program(
        functions=[
            ast.RegFunction(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                terminal=True,
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
                terminal=False,
                parameters=[],
                statements=[],
            ),
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3010.validate_called_symbol_termination(relationships)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3010
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20


def can_service_non_terminal_caller_symbol_not_last_call():
    program = ast.Program(
        functions=[
            ast.RegFunction(
                ref=src.Span(offset=1, length=20),
                name=b"bar",
                terminal=True,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=12, length=20),
                        name=b"foo2",
                        arguments=[],
                    ),
                    ast.CallStatement(
                        ref=src.Span(offset=22, length=25),
                        name=b"foo1",
                        arguments=[],
                    ),
                ],
            ),
            ast.RegFunction(
                ref=src.Span(offset=30, length=10),
                name=b"foo1",
                terminal=True,
                parameters=[],
                statements=[],
            ),
            ast.RegFunction(
                ref=src.Span(offset=30, length=10),
                name=b"foo2",
                terminal=False,
                parameters=[],
                statements=[],
            ),
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3010.validate_called_symbol_termination(relationships)

    assert len(diagnostics) == 0
