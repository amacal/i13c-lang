from i13c.sem import model, syntax
from tests.sem import prepare_program


def can_build_live_flowgraph_without_need_of_pruning():
    _, program = prepare_program("""
            asm halt() noreturn { syscall; }
            fn main() { halt(); }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic.live.flowgraph_by_function.size() == 1
    fid, flowgraph = semantic.live.flowgraph_by_function.peak()

    main = semantic.basic.functions.get(fid)
    assert len(main.statements) == 1

    cid = main.statements[0]

    assert flowgraph.entry in flowgraph.edges
    assert flowgraph.exit not in flowgraph.edges

    successors = flowgraph.edges.get(cid)

    assert successors is not None
    assert successors == []


def can_remove_callsite_after_terminal_call():
    _, program = prepare_program("""
            asm halt() noreturn { syscall; }
            fn main() noreturn { halt(); ignored(); }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic.live.flowgraph_by_function.size() == 1
    fid, flowgraph = semantic.live.flowgraph_by_function.peak()

    main = semantic.basic.functions.get(fid)
    assert len(main.statements) == 2

    cid = main.statements[0]

    assert flowgraph.entry in flowgraph.edges
    assert flowgraph.exit not in flowgraph.edges

    successors = flowgraph.edges.get(cid)

    assert successors is not None
    assert successors == []
