from i13c import ast, src
from i13c.sem import literal, model, syntax


def can_build_semantic_model_literals():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=0, length=10),
                name=b"main",
                noreturn=False,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=11, length=20),
                        name=b"foo",
                        arguments=[
                            ast.IntegerLiteral(
                                ref=src.Span(offset=31, length=40),
                                value=1142,
                            ),
                        ],
                    )
                ],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    literals = semantic.literals

    assert len(literals) == 1
    id, value = literals.popitem()

    assert isinstance(id, literal.LiteralId)
    assert isinstance(value, literal.Literal)

    assert value.kind == b"hex"
    assert isinstance(value.target, literal.Hex)

    assert value.target.value == 1142
    assert value.target.width == 16
