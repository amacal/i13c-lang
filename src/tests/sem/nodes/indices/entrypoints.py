from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.indices.entrypoints import EntryPoint
from tests.sem import prepare_program


def can_reject_function_with_arguments():
    _, program = prepare_program("""
        fn main(arg1: u32) noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 0


def can_accept_terminal_function():
    _, program = prepare_program("""
        asm exit() noreturn { }
        fn main() noreturn { exit(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 1
    _, value = entrypoints.peak()

    assert isinstance(value, EntryPoint)
    assert value.kind == b"function"

    assert isinstance(value.target, FunctionId)

    function = semantic.basic.functions.get(value.target)
    assert function.identifier.name == b"main"


def can_reject_snippet_with_arguments():
    _, program = prepare_program("""
        asm main(arg1@rax: u32) noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 0


def can_reject_terminal_snippet():
    _, program = prepare_program("""
        asm main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    entrypoints = semantic.live.entrypoints

    assert entrypoints.size() == 0
