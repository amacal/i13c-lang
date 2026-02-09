from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.indices.controlflows import FlowEntry, FlowExit, FlowGraph
from tests.sem import prepare_program


def can_do_nothing_without_any_function():
    _, program = prepare_program("""
            asm main() noreturn { }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 0


def can_build_flowgraph_for_a_function_without_any_statement():
    _, program = prepare_program("""
            fn main() { }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 1
    id, flow = values.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(flow, FlowGraph)

    assert isinstance(flow.entry, FlowEntry)
    assert isinstance(flow.exit, FlowExit)

    assert len(flow.forward) == 1
    assert len(flow.backward) == 1

    finput, foutputs = next(iter(flow.forward.items()))
    binput, boutputs = next(iter(flow.backward.items()))

    assert finput == flow.entry
    assert len(foutputs) == 1

    assert binput == flow.exit
    assert len(boutputs) == 1

    assert foutputs[0] == flow.exit
    assert boutputs[0] == flow.entry


def can_build_flowgraph_for_a_function_with_a_single_statement():
    _, program = prepare_program("""
            fn main() noreturn { foo(); }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 1
    id, flow = values.peak()

    assert isinstance(id, FunctionId)
    assert isinstance(flow, FlowGraph)

    assert isinstance(flow.entry, FlowEntry)
    assert isinstance(flow.exit, FlowExit)

    assert len(flow.forward) == 2
    assert len(flow.backward) == 2

    fn1s = flow.forward.get(flow.entry)
    bn1s = flow.backward.get(flow.exit)

    assert fn1s is not None and len(fn1s) == 1
    assert isinstance(fn1s[0], CallSiteId)

    assert bn1s is not None and len(bn1s) == 1
    assert isinstance(bn1s[0], CallSiteId)

    assert semantic.basic.callsites.get(fn1s[0]).callee.name == b"foo"
    assert semantic.basic.callsites.get(bn1s[0]).callee.name == b"foo"

    fn2s = flow.forward.get(fn1s[0])
    assert fn2s is not None and len(fn2s) == 1
    assert fn2s[0] == flow.exit

    bn2s = flow.backward.get(bn1s[0])
    assert bn2s is not None and len(bn2s) == 1
    assert bn2s[0] == flow.entry


def can_build_flowgraph_for_a_function_with_multiple_statements_ordered():
    _, program = prepare_program("""
            fn main() { foo(); bar(); baz(); }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    values = semantic.indices.flowgraph_by_function

    assert values.size() == 1
    _, flow = values.peak()

    assert isinstance(flow.entry, FlowEntry)
    assert isinstance(flow.exit, FlowExit)

    first = flow.forward.get(flow.entry)
    assert first is not None and len(first) == 1

    foo = first[0]
    assert isinstance(foo, CallSiteId)

    second = flow.forward.get(foo)
    assert second is not None and len(second) == 1

    bar = second[0]
    assert isinstance(bar, CallSiteId)

    third = flow.forward.get(bar)
    assert third is not None and len(third) == 1

    baz = third[0]
    assert isinstance(baz, CallSiteId)

    last = flow.forward.get(baz)
    assert last is not None and len(last) == 1
    assert last[0] == flow.exit

    assert semantic.basic.callsites.get(foo).callee.name == b"foo"
    assert semantic.basic.callsites.get(bar).callee.name == b"bar"
    assert semantic.basic.callsites.get(baz).callee.name == b"baz"
