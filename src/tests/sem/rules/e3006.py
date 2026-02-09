from i13c import err, semantic
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_detect_duplicated_snippet_names():
    source, program = prepare_program("""
            asm main() noreturn {
                syscall;
            }

            asm main() {
                syscall;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3006.validate_duplicated_function_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3006
    assert source.extract(diagnostic.ref) == b"main()"


def can_detect_duplicated_function_names():
    source, program = prepare_program("""
            fn main() noreturn {
            }

            fn main() {
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3006.validate_duplicated_function_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3006
    assert source.extract(diagnostic.ref) == b"main()"


def can_detect_duplicated_mixed_function_names():
    source, program = prepare_program("""
            asm main() {
                syscall;
            }

            fn main() {
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3006.validate_duplicated_function_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3006
    assert source.extract(diagnostic.ref) == b"main()"
