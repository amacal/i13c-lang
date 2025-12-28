from i13c.sem import syntax
from i13c.sem import model, function, snippet
from i13c import ast, src


def can_build_callgraphs_from_single_main():
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
    callgraph = semantic.callgraph

    assert len(callgraph) == 1
    target, callees = callgraph.popitem()

    assert isinstance(target, function.FunctionId)
    caller = semantic.functions[target]

    assert caller.identifier.name == b"main"
    assert len(callees) == 0


def can_build_callgraphs_from_main_calling_snippet():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"foo",
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
                        name=b"foo",
                        arguments=[],
                    )
                ],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callgraph = semantic.callgraph
    entrypoint = semantic.entrypoints[0]

    assert len(callgraph) == 2
    assert isinstance(entrypoint.target, function.FunctionId)

    callees = callgraph[entrypoint.target]
    caller = semantic.functions[entrypoint.target]

    assert caller.identifier.name == b"main"
    assert len(callees) == 1

    assert isinstance(callees[0], snippet.SnippetId)
    callee = semantic.snippets[callees[0]]

    assert callee.identifier.name == b"foo"
