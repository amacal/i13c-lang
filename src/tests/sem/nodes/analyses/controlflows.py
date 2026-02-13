from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_build_live_flowgraph_without_need_of_pruning():
    _, program = prepare_program("""
        asm halt() { syscall; }
        fn main() { halt(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic.live.flowgraph_by_function.size() == 1
    fid, flowgraph = semantic.live.flowgraph_by_function.peak()

    main = semantic.basic.functions.get(fid)
    assert len(main.statements) == 1

    assert flowgraph.entry in flowgraph.forward
    assert flowgraph.exit not in flowgraph.forward

    assert flowgraph.entry not in flowgraph.backward
    assert flowgraph.exit in flowgraph.backward

    cid = main.statements[0]
    successors = flowgraph.forward.get(cid)
    predecessors = flowgraph.backward.get(cid)

    assert successors is not None
    assert successors == [flowgraph.exit]

    assert predecessors is not None
    assert predecessors == [flowgraph.entry]


def can_remove_callsite_after_terminal_call():
    _, program = prepare_program("""
        asm halt() noreturn { syscall; }
        fn main() noreturn { halt(); ignored(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic.live.flowgraph_by_function.size() == 1
    fid, flowgraph = semantic.live.flowgraph_by_function.peak()

    main = semantic.basic.functions.get(fid)
    assert len(main.statements) == 2

    assert flowgraph.entry in flowgraph.forward
    assert flowgraph.exit not in flowgraph.forward

    assert flowgraph.entry not in flowgraph.backward
    assert flowgraph.exit not in flowgraph.backward

    cid = main.statements[0]
    successors = flowgraph.forward.get(cid)
    predecessors = flowgraph.backward.get(cid)

    assert successors is not None
    assert successors == []

    assert predecessors is not None
    assert predecessors == [flowgraph.entry]
