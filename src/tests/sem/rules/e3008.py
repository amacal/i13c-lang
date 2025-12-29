from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_missing_called_symbol():
    source, program = prepare_program(
        """
            fn main() {
                foo();
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3008.validate_called_symbol_exists(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3008
    assert source.extract(diagnostic.ref) == b"foo()"
