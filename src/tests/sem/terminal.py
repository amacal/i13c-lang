from i13c import ast, src
from i13c.sem import function, model, syntax, terminal


def can_build_semantic_model_terminalities_empty():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=0, length=10),
                name=b"main",
                noreturn=False,
                parameters=[],
                statements=[],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.function_terminalities

    assert len(terminalities) == 1
    id, terminality = terminalities.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(terminality, terminal.Terminality)

    assert terminality.noreturn is False


def can_build_semantic_model_terminalities_calls_terminal():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"exit_snippet",
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
                noreturn=False,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=11, length=20),
                        name=b"exit_snippet",
                        arguments=[],
                    )
                ],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.function_terminalities

    assert len(terminalities) == 1
    id, terminality = terminalities.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(terminality, terminal.Terminality)

    assert terminality.noreturn is True


def can_build_semantic_model_terminalities_calls_non_terminal():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"exit",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[],
            )
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=0, length=10),
                name=b"main",
                noreturn=False,
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

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.function_terminalities

    assert len(terminalities) == 1
    id, terminality = terminalities.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(terminality, terminal.Terminality)

    assert terminality.noreturn is False
