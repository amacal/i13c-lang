from i13c import ast, src
from i13c.sem import function, model, syntax


def can_build_semantic_model_functions():
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
                                ref=src.Span(offset=21, length=30),
                                value=42,
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
    functions = semantic.functions

    assert len(functions) == 1
    id, value = functions.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(value, function.Function)

    assert value.identifier.name == b"main"
    assert value.noreturn is False

    assert len(value.statements) == 1
    sid = syntax.NodeId(value=value.statements[0].value)

    statement = graph.nodes.statements.get_by_id(sid)
    assert isinstance(statement, ast.CallStatement)

    assert statement.name == b"foo"
    assert len(statement.arguments) == 1
