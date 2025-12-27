from i13c import ast, src
from i13c.sem import callsite, model, resolve, snippet, syntax


def can_build_semantic_model_accepted_resolutions_for_snippet():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"foo",
                noreturn=False,
                slots=[
                    ast.Slot(
                        name=b"arg1",
                        type=ast.Type(name=b"u32"),
                        bind=ast.Register(name=b"rax"),
                    )
                ],
                clobbers=[],
                instructions=[],
            )
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=10),
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
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0
    callables = value.accepted[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_build_semantic_model_rejected_resolutions_for_snippet_due_to_wrong_arity_much():
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
                ref=src.Span(offset=1, length=10),
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
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"wrong-arity"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_build_semantic_model_rejected_resolutions_for_snippet_due_to_wrong_arity_less():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"foo",
                noreturn=False,
                slots=[
                    ast.Slot(
                        name=b"arg1",
                        type=ast.Type(name=b"u32"),
                        bind=ast.Register(name=b"rax"),
                    )
                ],
                clobbers=[],
                instructions=[],
            )
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=10),
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
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"wrong-arity"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_build_semantic_model_rejected_resolutions_for_snippet_due_to_wrong_hex_width():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"foo",
                noreturn=False,
                slots=[
                    ast.Slot(
                        name=b"arg1",
                        type=ast.Type(name=b"u8"),
                        bind=ast.Register(name=b"rax"),
                    )
                ],
                clobbers=[],
                instructions=[],
            )
        ],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=10),
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
                                value=0x1234,
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
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"type-mismatch"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"
