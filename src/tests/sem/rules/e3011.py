from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_semantic_model


def can_detect_incorrect_argument_count_for_a_call_less():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
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
            ast.Function(
                ref=src.Span(offset=30, length=10),
                name=b"foo",
                terminal=True,
                parameters=[
                    ast.Parameter(
                        name=b"x",
                        type=ast.Type(name=b"u8"),
                    )
                ],
                statements=[],
            ),
        ],
    )

    graph = build_graph(program)
    model = build_semantic_model(graph)
    diagnostics = sem.e3011.validate_called_arguments_count(graph, model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
