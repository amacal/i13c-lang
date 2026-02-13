from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.indices.terminalities import Terminality
from tests.sem import prepare_program


def can_do_nothing_without_any_function():
    _, program = prepare_program("""
        asm main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 0


def can_build_terminalities_for_single_function_without_any_statement():
    _, program = prepare_program("""
        fn main() { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is False


def can_build_terminalities_for_a_function_calling_terminal_snippet():
    _, program = prepare_program("""
        asm exit() noreturn { }
        fn main() { exit(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is True


def can_build_terminalities_for_a_function_calling_non_terminal_snippet():
    _, program = prepare_program("""
        asm exit() { }
        fn main() { exit(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is False


def can_do_nothing_when_callsite_is_not_resolved():
    _, program = prepare_program("""
        fn main() { unknown(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 0


def can_do_nothing_for_ambiguous_callsites():
    _, program = prepare_program("""
        asm exit() noreturn { }
        asm exit() { }
        fn main() { exit(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 0
