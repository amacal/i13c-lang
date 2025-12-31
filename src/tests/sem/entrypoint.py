from i13c.sem import entrypoint, function, model, snippet, syntax
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

    assert entrypoints.size() == 1
    _, value = entrypoints.pop()

    assert isinstance(value, entrypoint.EntryPoint)
    assert value.kind == b"function"

    assert isinstance(value.target, function.FunctionId)
    fid = syntax.NodeId(value=value.target.value)

    target = graph.functions.get_by_id(fid)
    assert target.name == b"main"


def can_reject_snippet_with_arguments():
    _, program = prepare_program(
        """
            asm main(arg1@rax: u32) noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.entrypoints

    assert entrypoints.size() == 0


def can_accept_snippet_as_entrypoint():
    _, program = prepare_program(
        """
            asm main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.entrypoints

    assert entrypoints.size() == 1
    _, value = entrypoints.pop()

    assert isinstance(value, entrypoint.EntryPoint)
    assert value.kind == b"snippet"

    assert isinstance(value.target, snippet.SnippetId)
    sid = syntax.NodeId(value=value.target.value)

    target = graph.snippets.get_by_id(sid)
    assert target.name == b"main"
