from i13c import err, semantic
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_survive_existing_entrypoint():
    _, program = prepare_program("""
            asm exit() noreturn { }
            fn main() noreturn { exit(); }
        """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 0


def can_detect_nonexistent_entrypoint_even_if_function_is_called_main2():
    source, program = prepare_program("""
            fn main2() noreturn { }
        """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert source.extract(diagnostic.ref) == b""


def can_reject_main_as_entrypoint_when_noreturn_is_false():
    source, program = prepare_program("""
            fn main() { }
        """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert source.extract(diagnostic.ref) == b""


def can_accept_main_when_terminality_is_unresolved():
    _, program = prepare_program("""
            fn main() noreturn { missing(); }
        """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3011.validate_entrypoint_exists(model)

    assert len(diagnostics) == 0
