from i13c import ast, src
from i13c.sem import flows, function, model, syntax


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
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    flowgraphs = semantic.function_flowgraphs

    assert len(flowgraphs) == 1
    id, flow = flowgraphs.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(flow, flows.FlowGraph)

    assert isinstance(flow.entry, flows.FlowEntry)
    assert isinstance(flow.exit, flows.FlowExit)

    assert len(flow.edges) == 1
    input, outputs = flow.edges.popitem()

    assert input == flow.entry
    assert len(outputs) == 1

    assert outputs[0] == flow.exit


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
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    flowgraphs = semantic.function_flowgraphs

    assert len(flowgraphs) == 1
    id, flow = flowgraphs.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(flow, flows.FlowGraph)

    assert isinstance(flow.entry, flows.FlowEntry)
    assert isinstance(flow.exit, flows.FlowExit)

    assert len(flow.edges) == 2
    n1s = flow.edges.get(flow.entry)

    assert n1s is not None and len(n1s) == 1
    assert isinstance(n1s[0], model.CallSiteId)

    assert semantic.callsites[n1s[0]].callee.name == b"foo"

    n2s = flow.edges.get(n1s[0])
    assert n2s is not None and len(n2s) == 1
    assert n2s[0] == flow.exit
