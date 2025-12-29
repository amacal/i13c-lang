from i13c.sem import entrypoint, function, model, syntax
from tests.sem import prepare_program


def can_build_entrypoints_for_valid_main_function():
    _, program = prepare_program(
        """
            asm exit() noreturn { }
            fn main() noreturn { exit(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.entrypoints

    assert len(entrypoints) == 1
    value = entrypoints[0]

    assert isinstance(value, entrypoint.EntryPoint)
    assert value.kind == b"function"

    assert isinstance(value.target, function.FunctionId)
    fid = syntax.NodeId(value=value.target.value)

    target = graph.nodes.functions.get_by_id(fid)
    assert target.name == b"main"
