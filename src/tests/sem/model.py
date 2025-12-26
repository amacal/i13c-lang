from i13c import ast, src
from i13c.sem import model, syntax


def can_build_semantic_model_snippets():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=10),
                name=b"main",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=11, length=15),
                        mnemonic=ast.Mnemonic(name=b"mov"),
                        operands=[
                            ast.Register(name=b"rax"),
                            ast.Immediate(value=0x1234),
                        ],
                    )
                ],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)
    snippets = model.build_semantic_graph_snippets(graph)

    assert len(snippets) == 1
    id, snippet = snippets.popitem()

    assert isinstance(id, model.SnippetId)
    assert isinstance(snippet, model.Snippet)

    assert snippet.identifier.name == b"main"
    assert snippet.noreturn is False

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert isinstance(instruction, model.Instruction)
    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    assert instruction.operands[0].kind == b"register"
    assert isinstance(instruction.operands[0].target, model.Register)
    assert instruction.operands[0].target.name == b"rax"

    assert instruction.operands[1].kind == b"immediate"
    assert isinstance(instruction.operands[1].target, model.Immediate)
    assert instruction.operands[1].target.value == 0x1234


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
    literals = model.build_semantic_graph_literals(graph)

    assert len(literals) == 1
    id, literal = literals.popitem()

    assert isinstance(id, model.LiteralId)
    assert isinstance(literal, model.Literal)

    assert literal.kind == b"hex"
    assert isinstance(literal.target, model.Hex)

    assert literal.target.value == 1142
    assert literal.target.width == 16


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
    callsites = model.build_semantic_graph_callsites(graph)

    assert len(callsites) == 1
    id, callsite = callsites.popitem()

    assert isinstance(id, model.CallSiteId)
    assert isinstance(callsite, model.CallSite)

    assert callsite.callee.name == b"foo"
    assert len(callsite.arguments) == 1

    argument = callsite.arguments[0]
    assert argument.kind == b"literal"

    assert isinstance(argument.target, model.LiteralId)
    lid = syntax.NodeId(value=argument.target.value)

    literal = graph.nodes.literals.get_by_id(lid)
    assert literal.value == 42


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
    functions = model.build_semantic_graph_functions(graph)

    assert len(functions) == 1
    id, function = functions.popitem()

    assert isinstance(id, model.FunctionId)
    assert isinstance(function, model.Function)

    assert function.identifier.name == b"main"
    assert function.noreturn is False

    assert len(function.statements) == 1
    sid = syntax.NodeId(value=function.statements[0].value)

    statement = graph.nodes.statements.get_by_id(sid)
    assert isinstance(statement, ast.CallStatement)

    assert statement.name == b"foo"
    assert len(statement.arguments) == 1


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

    literals = model.build_semantic_graph_literals(graph)
    functions = model.build_semantic_graph_functions(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    callsites = model.build_semantic_graph_callsites(graph)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    assert len(resolutions) == 1
    id, resolution = resolutions.popitem()

    assert isinstance(id, model.CallSiteId)
    assert isinstance(resolution, model.Resolution)

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0
    callables = resolution.accepted[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, model.SnippetId)

    snippet = snippets[callables.target]
    assert snippet.identifier.name == b"foo"


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

    literals = model.build_semantic_graph_literals(graph)
    functions = model.build_semantic_graph_functions(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    callsites = model.build_semantic_graph_callsites(graph)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    assert len(resolutions) == 1
    id, resolution = resolutions.popitem()

    assert isinstance(id, model.CallSiteId)
    assert isinstance(resolution, model.Resolution)

    assert len(resolution.rejected) == 1
    assert len(resolution.accepted) == 0

    assert resolution.rejected[0].reason == b"wrong-arity"
    callables = resolution.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, model.SnippetId)

    snippet = snippets[callables.target]
    assert snippet.identifier.name == b"foo"


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

    literals = model.build_semantic_graph_literals(graph)
    functions = model.build_semantic_graph_functions(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    callsites = model.build_semantic_graph_callsites(graph)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    assert len(resolutions) == 1
    id, resolution = resolutions.popitem()

    assert isinstance(id, model.CallSiteId)
    assert isinstance(resolution, model.Resolution)

    assert len(resolution.rejected) == 1
    assert len(resolution.accepted) == 0

    assert resolution.rejected[0].reason == b"wrong-arity"
    callables = resolution.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, model.SnippetId)

    snippet = snippets[callables.target]
    assert snippet.identifier.name == b"foo"


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

    literals = model.build_semantic_graph_literals(graph)
    functions = model.build_semantic_graph_functions(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    callsites = model.build_semantic_graph_callsites(graph)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    assert len(resolutions) == 1
    id, resolution = resolutions.popitem()

    assert isinstance(id, model.CallSiteId)
    assert isinstance(resolution, model.Resolution)

    assert len(resolution.rejected) == 1
    assert len(resolution.accepted) == 0

    assert resolution.rejected[0].reason == b"type-mismatch"
    callables = resolution.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, model.SnippetId)

    snippet = snippets[callables.target]
    assert snippet.identifier.name == b"foo"


def can_build_semantic_model_flowgraphs_no_statements():
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
    functions = model.build_semantic_graph_functions(graph)
    flowgraphs = model.build_semantic_graph_flowgraphs(functions)

    assert len(flowgraphs) == 1
    id, flowgraph = flowgraphs.popitem()

    assert isinstance(id, model.FunctionId)
    assert isinstance(flowgraph, model.FlowGraph)

    assert isinstance(flowgraph.entry, model.FlowEntry)
    assert isinstance(flowgraph.exit, model.FlowExit)

    assert len(flowgraph.edges) == 1
    input, outputs = flowgraph.edges.popitem()

    assert input == flowgraph.entry
    assert len(outputs) == 1

    assert outputs[0] == flowgraph.exit


def can_build_semantic_model_flowgraphs_single_statement():
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
                        arguments=[],
                    )
                ],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)
    functions = model.build_semantic_graph_functions(graph)
    callsites = model.build_semantic_graph_callsites(graph)
    flowgraphs = model.build_semantic_graph_flowgraphs(functions)

    assert len(flowgraphs) == 1
    id, flowgraph = flowgraphs.popitem()

    assert isinstance(id, model.FunctionId)
    assert isinstance(flowgraph, model.FlowGraph)

    assert isinstance(flowgraph.entry, model.FlowEntry)
    assert isinstance(flowgraph.exit, model.FlowExit)

    assert len(flowgraph.edges) == 2
    n1s = flowgraph.edges.get(flowgraph.entry)

    assert n1s is not None and len(n1s) == 1
    assert isinstance(n1s[0], model.CallSiteId)

    assert callsites[n1s[0]].callee.name == b"foo"

    n2s = flowgraph.edges.get(n1s[0])
    assert n2s is not None and len(n2s) == 1
    assert n2s[0] == flowgraph.exit


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

    literals = model.build_semantic_graph_literals(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    functions = model.build_semantic_graph_functions(graph)
    callsites = model.build_semantic_graph_callsites(graph)
    flowgraphs = model.build_semantic_graph_flowgraphs(functions)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    terminalities = model.build_semantic_graph_terminalities(
        snippets, functions, flowgraphs, resolutions
    )

    assert len(terminalities) == 1
    id, terminality = terminalities.popitem()

    assert isinstance(id, model.FunctionId)
    assert isinstance(terminality, model.Terminality)

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

    literals = model.build_semantic_graph_literals(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    functions = model.build_semantic_graph_functions(graph)
    callsites = model.build_semantic_graph_callsites(graph)
    flowgraphs = model.build_semantic_graph_flowgraphs(functions)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    terminalities = model.build_semantic_graph_terminalities(
        snippets, functions, flowgraphs, resolutions
    )

    assert len(terminalities) == 1
    id, terminality = terminalities.popitem()

    assert isinstance(id, model.FunctionId)
    assert isinstance(terminality, model.Terminality)

    assert terminality.noreturn is True


def can_build_semantic_model_terminalities_calls_non_terminal():
    program = ast.Program(
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=31, length=10),
                name=b"exit_snippet",
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
                        name=b"exit_snippet",
                        arguments=[],
                    )
                ],
            )
        ],
    )

    graph = syntax.build_syntax_graph(program)

    literals = model.build_semantic_graph_literals(graph)
    snippets = model.build_semantic_graph_snippets(graph)
    functions = model.build_semantic_graph_functions(graph)
    callsites = model.build_semantic_graph_callsites(graph)
    flowgraphs = model.build_semantic_graph_flowgraphs(functions)

    resolutions = model.build_semantic_graph_resolutions(
        functions, snippets, callsites, literals
    )

    terminalities = model.build_semantic_graph_terminalities(
        snippets, functions, flowgraphs, resolutions
    )

    assert len(terminalities) == 1
    id, terminality = terminalities.popitem()

    assert isinstance(id, model.FunctionId)
    assert isinstance(terminality, model.Terminality)

    assert terminality.noreturn is False
