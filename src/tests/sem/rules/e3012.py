from i13c import err, semantic
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_detect_multiple_entrypoints():
    _, program = prepare_program("""
            asm exit() noreturn { }
            fn main() noreturn { }
            fn main() noreturn { exit(); }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3012.validate_entrypoint_is_single(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3012
    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 0
