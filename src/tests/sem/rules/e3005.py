from i13c import err, semantic
from i13c.semantic.model import build_semantic_graph
from i13c.semantic.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_duplicated_slot_clobbers():
    source, program = prepare_program("""
            asm main() clobbers rax, rbx, rax {
                syscall;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3005.validate_duplicated_snippet_clobbers(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert source.extract(diagnostic.ref) == b"main()"
