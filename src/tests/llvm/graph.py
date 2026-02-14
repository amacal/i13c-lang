from pytest import raises

from tests.llvm import GraphFixtureException, prepare_graph


def can_prepare_graph_from_a_valid_program():
    graph = prepare_graph("""
        asm exit() noreturn { syscall; }
        fn main() noreturn { exit(); }
    """)

    assert graph is not None


def can_raise_exception_if_program_has_semantic_errors():
    with raises(GraphFixtureException) as ex:
        prepare_graph("""
            fn main() { foo(0x123); }
        """)

    assert ex is not None
