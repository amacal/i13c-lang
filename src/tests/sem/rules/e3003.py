from i13c import err
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_detect_duplicated_slot_bindings():
    source, program = prepare_program("""
        asm main(code@rdi: u32, id@rdi: u16) noreturn { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3003")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3003
    assert source.extract(diagnostic.ref) == b"main(code@rdi: u32, id@rdi: u16)"


def can_ignore_immediate_slot_bindings():
    _, program = prepare_program("""
        asm first(code@imm: u32, id@imm: u16) noreturn { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3003")

    assert len(diagnostics) == 0
