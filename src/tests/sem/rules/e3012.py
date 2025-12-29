from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_multiple_entrypoints():
    _, program = prepare_program(
        """
            asm exit() noreturn { }
            asm main() noreturn { }
            fn main() noreturn { exit(); }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3012.validate_entrypoint_is_single(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3012
    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 0
