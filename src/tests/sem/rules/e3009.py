from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_non_snippet_called_symbol():
    source, program = prepare_program(
        """
            fn foo() {
            }

            fn main() {
                foo();
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3009.validate_called_symbol_is_snippet(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3009
    assert source.extract(diagnostic.ref) == b"foo()"
