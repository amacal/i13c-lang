from i13c import err, semantic
from i13c.semantic.model import build_semantic_graph
from i13c.semantic.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_duplicated_slot_bindings():
    source, program = prepare_program("""
            asm main(code@rdi: u32, id@rdi: u16) noreturn {
                syscall;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3003.validate_duplicated_slot_bindings(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3003
    assert source.extract(diagnostic.ref) == b"main(code@rdi: u32, id@rdi: u16)"


def can_ignore_immediate_slot_bindings():
    _, program = prepare_program("""
            asm first(code@imm: u32, id@imm: u16) noreturn {
                syscall;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3003.validate_duplicated_slot_bindings(model)

    assert len(diagnostics) == 0
