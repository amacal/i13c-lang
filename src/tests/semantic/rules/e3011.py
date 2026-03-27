from i13c import err
from i13c.graph.nodes import run as run_graph
from tests.semantic import prepare_program


def can_survive_existing_entrypoint():
    _, program = prepare_program("""
            asm exit() noreturn { }
            fn main() noreturn { exit(); }
        """)

    diagnostics = run_graph(program).rule_by_name("e3011")

    assert len(diagnostics) == 0


def can_detect_nonexistent_entrypoint_even_if_function_is_called_main2():
    source, program = prepare_program("""
            fn main2() noreturn { }
        """)

    diagnostics = run_graph(program).rule_by_name("e3011")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert source.extract(diagnostic.ref) == b""


def can_reject_main_as_entrypoint_when_noreturn_is_false():
    source, program = prepare_program("""
            fn main() { }
        """)

    diagnostics = run_graph(program).rule_by_name("e3011")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3011
    assert source.extract(diagnostic.ref) == b""


def can_accept_main_when_terminality_is_unresolved():
    _, program = prepare_program("""
            fn main() noreturn { missing(); }
        """)

    diagnostics = run_graph(program).rule_by_name("e3011")

    assert len(diagnostics) == 0
