from i13c.sem import flowgraphs, function, model, syntax
from tests.sem import prepare_program


def can_build_semantic_model_flowgraphs_no_statements():
    _, program = prepare_program(
        """
            fn main() { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    values = semantic.function_flowgraphs

    assert len(values) == 1
    id, flow = values.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(flow, flowgraphs.FlowGraph)

    assert isinstance(flow.entry, flowgraphs.FlowEntry)
    assert isinstance(flow.exit, flowgraphs.FlowExit)

    assert len(flow.edges) == 1
    input, outputs = flow.edges.popitem()

    assert input == flow.entry
    assert len(outputs) == 1

    assert outputs[0] == flow.exit


def can_build_semantic_model_flowgraphs_single_statement():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    values = semantic.function_flowgraphs

    assert len(values) == 1
    id, flow = values.popitem()

    assert isinstance(id, function.FunctionId)
    assert isinstance(flow, flowgraphs.FlowGraph)

    assert isinstance(flow.entry, flowgraphs.FlowEntry)
    assert isinstance(flow.exit, flowgraphs.FlowExit)

    assert len(flow.edges) == 2
    n1s = flow.edges.get(flow.entry)

    assert n1s is not None and len(n1s) == 1
    assert isinstance(n1s[0], model.CallSiteId)

    assert semantic.callsites[n1s[0]].callee.name == b"foo"

    n2s = flow.edges.get(n1s[0])
    assert n2s is not None and len(n2s) == 1
    assert n2s[0] == flow.exit
