from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_duplicated_slot_clobbers():
    source, program = prepare_program(
        """
            asm main() clobbers rax, rbx, rax {
                syscall;
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3005.validate_duplicated_snippet_clobbers(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert source.extract(diagnostic.ref) == b"main()"
