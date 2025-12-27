from i13c import ast, src
from i13c.sem import callsite, model, syntax


def can_build_semantic_model_callsites():
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
    callsites = semantic.callsites

    assert len(callsites) == 1
    id, value = callsites.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, callsite.CallSite)

    assert value.callee.name == b"foo"
    assert len(value.arguments) == 1

    argument = value.arguments[0]
    assert argument.kind == b"literal"

    assert isinstance(argument.target, callsite.LiteralId)
    lid = syntax.NodeId(value=argument.target.value)

    literal = graph.nodes.literals.get_by_id(lid)
    assert literal.value == 42
