from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_detect_non_snippet_called_symbol():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=20),
                name=b"main",
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
            ast.Function(
                ref=src.Span(offset=30, length=10),
                name=b"foo",
                noreturn=True,
                parameters=[],
                statements=[],
            ),
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3009.validate_called_symbol_is_snippet(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3009
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
