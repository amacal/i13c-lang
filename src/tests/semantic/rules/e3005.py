from i13c import err
from i13c.graph.nodes import run as run_graph
from tests.semantic import prepare_program


def can_detect_duplicated_slot_clobbers():
    source, program = prepare_program("""
            asm main() clobbers rax, rbx, rax { syscall; }
        """)

    diagnostics = run_graph(program).rule_by_name("e3005")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert source.extract(diagnostic.ref) == b"main()"
