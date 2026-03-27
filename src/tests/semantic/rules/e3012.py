from i13c import err
from i13c.graph.nodes import run as run_graph
from tests.semantic import prepare_program


def can_detect_multiple_entrypoints():
    _, program = prepare_program("""
            asm exit() noreturn { }
            fn main() noreturn { }
            fn main() noreturn { exit(); }
        """)

    diagnostics = run_graph(program).rule_by_name("e3012")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3012
    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 0
