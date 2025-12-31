from i13c.sem import model, syntax
from tests.sem import prepare_program


def can_build_live_flowgraph_without_need_of_pruning():
    _, program = prepare_program(
        """
            asm halt() noreturn { syscall; }
            fn main() { halt(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert len(semantic.flowgraph_by_function_live) == 1
    fid, flowgraph_live = semantic.flowgraph_by_function_live.popitem()

    main = semantic.functions.get(fid)
    assert len(main.statements) == 1

    callsite_id = main.statements[0]

    assert flowgraph_live.entry in flowgraph_live.edges
    assert flowgraph_live.exit not in flowgraph_live.edges

    successors = flowgraph_live.edges.get(callsite_id)

    assert successors is not None
    assert successors == []
