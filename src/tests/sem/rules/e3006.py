from i13c import err, semantic
from i13c.semantic.model import build_semantic_graph
from i13c.semantic.syntax import build_syntax_graph
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

    model = build_semantic_graph(build_syntax_graph(program))
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

    model = build_semantic_graph(build_syntax_graph(program))
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

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3006.validate_duplicated_function_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3006
    assert source.extract(diagnostic.ref) == b"main()"
