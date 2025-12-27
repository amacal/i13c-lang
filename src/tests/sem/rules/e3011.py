from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_survive_existing_entrypoint():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=4),
                name=b"exit",
                noreturn=True,
                slots=[],
                clobbers=[],
                instructions=[],
            )
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=0, length=10),
                name=b"main",
                noreturn=True,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=11, length=20),
                        name=b"exit",
                        arguments=[],
                    )
                ],
            )
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 0


def can_detect_unexisting_entrypoint_even_if_function_is_called_main2():
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

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 0


def can_consider_main_as_entrypoint_when_noreturn_is_false():
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

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 0
