from i13c import err, semantic
from i13c.semantic.model import build_semantic_graph
from i13c.semantic.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_duplicated_slot_names():
    source, program = prepare_program("""
            asm main(code@rdi: u32, code@rax: u16) noreturn {
                syscall;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3004.validate_duplicated_parameter_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert source.extract(diagnostic.ref) == b"main(code@rdi: u32, code@rax: u16)"


def can_detect_duplicated_parameter_names():
    source, program = prepare_program("""
            fn aux(code: u32, code: u16) {
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3004.validate_duplicated_parameter_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert source.extract(diagnostic.ref) == b"aux(code: u32, code: u16)"
