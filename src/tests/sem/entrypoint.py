from i13c import ast, src
from i13c.sem import entrypoint, function, model, syntax


def can_build_entrypoints_for_valid_main_function():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
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

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.entrypoints

    assert len(entrypoints) == 1
    value = entrypoints[0]

    assert isinstance(value, entrypoint.EntryPoint)
    assert value.kind == b"function"

    assert isinstance(value.target, function.FunctionId)
    fid = syntax.NodeId(value=value.target.value)

    target = graph.nodes.functions.get_by_id(fid)
    assert target.name == b"main"
