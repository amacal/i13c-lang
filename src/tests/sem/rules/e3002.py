from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_invalid_operand_types_of_mov():
    _, program = prepare_program(
        """
            asm main() noreturn {
                mov 0x1234, 0x5678;
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3002.validate_assembly_operand_types(model)

    assert len(diagnostics) == 4

    # all of them are related to E3002
    for diagnostic in diagnostics:
        assert diagnostic.code == err.ERROR_3002
        assert diagnostic.ref.offset == 51
        assert diagnostic.ref.length == 19
