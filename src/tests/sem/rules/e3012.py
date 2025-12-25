from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_model


def can_survive_terminal_entrypoint():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=0, length=10),
                name=b"main",
                noreturn=True,
                parameters=[],
                statements=[],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3012.validate_entrypoint_never_returns(model)

    assert len(diagnostics) == 0


def can_detect_non_terminal_entrypoint():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=12, length=10),
                name=b"main",
                noreturn=False,
                parameters=[],
                statements=[],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3012.validate_entrypoint_never_returns(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3012
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 10
