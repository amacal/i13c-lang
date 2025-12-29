from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_immediate_out_of_range():
    source, program = prepare_program(
        """
            asm main() noreturn {
                mov rax, 0x123456789012345678;
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3001.validate_immediate_out_of_range(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3001
    assert source.extract(diagnostic.ref) == b"mov rax, 0x123456789012345678;"
