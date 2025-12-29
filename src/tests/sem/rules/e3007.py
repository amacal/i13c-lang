from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_integer_literal_out_of_range():
    source, program = prepare_program(
        """
            fn main() {
                foo(0x1ffffffffffffffff);
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3007.validate_integer_literal_out_of_range(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert source.extract(diagnostic.ref) == b"0x1ffffffffffffffff"
