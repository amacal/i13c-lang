from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_survive_non_terminal_callee_symbol():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=10),
                name=b"foo",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[],
            ),
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=20),
                name=b"bar",
                noreturn=False,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=12, length=20),
                        name=b"foo",
                        arguments=[],
                    )
                ],
            ),
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3010.validate_called_symbol_termination(model)

    assert len(diagnostics) == 0


def can_detect_non_terminal_caller_symbol():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=10),
                name=b"foo",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[],
            ),
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                noreturn=True,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=12, length=20),
                        name=b"foo",
                        arguments=[],
                    )
                ],
            ),
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3010.validate_called_symbol_termination(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3010
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


def can_survive_non_terminal_caller_symbol_not_last_call():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=10),
                name=b"foo1",
                noreturn=True,
                slots=[],
                clobbers=[],
                instructions=[],
            ),
            ast.Snippet(
                ref=src.Span(offset=10, length=10),
                name=b"foo2",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[],
            ),
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=20),
                name=b"bar",
                noreturn=True,
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
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3010.validate_called_symbol_termination(model)

    assert len(diagnostics) == 0
