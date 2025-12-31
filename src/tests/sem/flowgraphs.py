from i13c.sem import callsite, flowgraphs, function, model, syntax
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
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 1
    id, flow = values.pop()

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
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 1
    id, flow = values.pop()

    assert isinstance(id, function.FunctionId)
    assert isinstance(flow, flowgraphs.FlowGraph)

    assert isinstance(flow.entry, flowgraphs.FlowEntry)
    assert isinstance(flow.exit, flowgraphs.FlowExit)

    assert len(flow.edges) == 2
    n1s = flow.edges.get(flow.entry)

    assert n1s is not None and len(n1s) == 1
    assert isinstance(n1s[0], model.CallSiteId)

    assert semantic.basic.callsites.get(n1s[0]).callee.name == b"foo"

    n2s = flow.edges.get(n1s[0])
    assert n2s is not None and len(n2s) == 1
    assert n2s[0] == flow.exit


def can_build_flow_with_multiple_statements_ordered():
    _, program = prepare_program(
        """
            fn main() { foo(); bar(); baz(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 1
    _, flow = values.pop()

    assert isinstance(flow.entry, flowgraphs.FlowEntry)
    assert isinstance(flow.exit, flowgraphs.FlowExit)

    first = flow.edges.get(flow.entry)
    assert first is not None and len(first) == 1

    foo = first[0]
    assert isinstance(foo, callsite.CallSiteId)

    second = flow.edges.get(foo)
    assert second is not None and len(second) == 1

    bar = second[0]
    assert isinstance(bar, callsite.CallSiteId)

    third = flow.edges.get(bar)
    assert third is not None and len(third) == 1

    baz = third[0]
    assert isinstance(baz, callsite.CallSiteId)

    last = flow.edges.get(baz)
    assert last is not None and len(last) == 1
    assert last[0] == flow.exit

    assert semantic.basic.callsites.get(foo).callee.name == b"foo"
    assert semantic.basic.callsites.get(bar).callee.name == b"bar"
    assert semantic.basic.callsites.get(baz).callee.name == b"baz"
