from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_model


def can_survive_existing_entrypoint():
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
    diagnostics = sem.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 0


def can_detect_unexisting_entrypoint():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=12, length=10),
                name=b"main2",
                noreturn=False,
                parameters=[],
                statements=[],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 0
