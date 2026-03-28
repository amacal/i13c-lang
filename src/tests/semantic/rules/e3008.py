from i13c.graph.nodes import run as run_graph
from tests.semantic import prepare_program


def can_detect_missing_called_symbol():
    source, program = prepare_program("""
            fn main() {
                foo();
            }
        """)

    diagnostics = run_graph(program).rule_by_name("e3008")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E3008"
    assert source.extract(diagnostic.ref) == b"foo()"
