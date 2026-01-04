from i13c.sem import model, syntax
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import SnippetId
from i13c.sem.typing.indices.entrypoints import EntryPoint
from tests.sem import prepare_program


def can_reject_function_with_arguments():
    _, program = prepare_program(
        """
            fn main(arg1: u32) noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 0


def can_accept_terminal_function():
    _, program = prepare_program(
        """
            asm exit() noreturn { }
            fn main() noreturn { exit(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 1
    _, value = entrypoints.pop()

    assert isinstance(value, EntryPoint)
    assert value.kind == b"function"

    assert isinstance(value.target, FunctionId)
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
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 0


def can_accept_terminal_snippet():
    _, program = prepare_program(
        """
            asm main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 1
    _, value = entrypoints.pop()

    assert isinstance(value, EntryPoint)
    assert value.kind == b"snippet"

    assert isinstance(value.target, SnippetId)
    sid = syntax.NodeId(value=value.target.value)

    target = graph.snippets.get_by_id(sid)
    assert target.name == b"main"
