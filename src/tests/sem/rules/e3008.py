from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_model


def can_detect_missing_called_symbol():
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
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3008.validate_called_symbol_exists(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3008
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
