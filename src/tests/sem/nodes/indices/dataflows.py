from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_do_nothing_without_any_function():
    _, program = prepare_program("""
            asm main() noreturn { }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    values = semantic.indices.dataflow_by_flownode

    assert values.size() == 0


def can_build_dataflow_for_a_function_without_any_parameters():
    _, program = prepare_program("""
            fn main() { }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    controlflows = semantic.indices.flowgraph_by_function

    assert controlflows.size() == 1
    _, flow = controlflows.pop()

    entry = semantic.indices.dataflow_by_flownode.get(flow.entry)
    exit = semantic.indices.dataflow_by_flownode.get(flow.exit)

    assert len(entry.declares) == 0
    assert len(entry.uses) == 0
    assert len(entry.drops) == 0

    assert len(exit.declares) == 0
    assert len(exit.uses) == 0
    assert len(exit.drops) == 0


def can_build_dataflow_for_a_function_with_single_parameter():
    _, program = prepare_program("""
            fn main(val: u8) { }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    controlflows = semantic.indices.flowgraph_by_function

    assert controlflows.size() == 1
    _, flow = controlflows.pop()

    entry = semantic.indices.dataflow_by_flownode.get(flow.entry)
    exit = semantic.indices.dataflow_by_flownode.get(flow.exit)

    assert len(entry.declares) == 1
    assert len(entry.uses) == 0
    assert len(entry.drops) == 0

    assert len(exit.declares) == 0
    assert len(exit.uses) == 0
    assert len(exit.drops) == 1


def can_build_dataflow_for_a_function_with_callsite_and_literal():
    _, program = prepare_program("""
            fn main() { foo(0x42); }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    controlflows = semantic.indices.flowgraph_by_function

    assert controlflows.size() == 1
    _, flow = controlflows.pop()

    assert semantic.basic.callsites.size() == 1
    cid, _ = semantic.basic.callsites.pop()

    entry = semantic.indices.dataflow_by_flownode.get(flow.entry)
    exit = semantic.indices.dataflow_by_flownode.get(flow.exit)
    callsite = semantic.indices.dataflow_by_flownode.get(cid)

    assert len(entry.declares) == 0
    assert len(entry.uses) == 0
    assert len(entry.drops) == 0

    assert len(exit.declares) == 0
    assert len(exit.uses) == 0
    assert len(exit.drops) == 0

    assert len(callsite.declares) == 0
    assert len(callsite.uses) == 0
    assert len(callsite.drops) == 0


def can_build_dataflow_for_a_function_with_callsite_and_identifier():
    _, program = prepare_program("""
            fn main(abc: u8) { foo(abc); }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    controlflows = semantic.indices.flowgraph_by_function

    assert controlflows.size() == 1
    _, flow = controlflows.pop()

    assert semantic.basic.callsites.size() == 1
    cid, _ = semantic.basic.callsites.pop()

    entry = semantic.indices.dataflow_by_flownode.get(flow.entry)
    exit = semantic.indices.dataflow_by_flownode.get(flow.exit)
    callsite = semantic.indices.dataflow_by_flownode.get(cid)

    assert len(entry.declares) == 1
    assert len(entry.uses) == 0
    assert len(entry.drops) == 0

    assert len(exit.declares) == 0
    assert len(exit.uses) == 0
    assert len(exit.drops) == 1

    assert len(callsite.declares) == 0
    assert len(callsite.uses) == 1
    assert len(callsite.drops) == 0


def can_build_dataflow_for_a_function_with_callsite_and_unresolved_identifier():
    _, program = prepare_program("""
            fn main() { foo(abc); }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    controlflows = semantic.indices.flowgraph_by_function

    assert controlflows.size() == 1
    _, flow = controlflows.pop()

    assert semantic.basic.callsites.size() == 1
    cid, _ = semantic.basic.callsites.pop()

    entry = semantic.indices.dataflow_by_flownode.get(flow.entry)
    exit = semantic.indices.dataflow_by_flownode.get(flow.exit)
    callsite = semantic.indices.dataflow_by_flownode.get(cid)

    assert len(entry.declares) == 0
    assert len(entry.uses) == 0
    assert len(entry.drops) == 0

    assert len(exit.declares) == 0
    assert len(exit.uses) == 0
    assert len(exit.drops) == 0

    assert len(callsite.declares) == 0
    assert len(callsite.uses) == 1
    assert len(callsite.drops) == 0
