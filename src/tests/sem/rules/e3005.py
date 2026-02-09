from i13c import err, semantic
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_detect_duplicated_slot_clobbers():
    source, program = prepare_program("""
            asm main() clobbers rax, rbx, rax {
                syscall;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3005.validate_duplicated_snippet_clobbers(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert source.extract(diagnostic.ref) == b"main()"
