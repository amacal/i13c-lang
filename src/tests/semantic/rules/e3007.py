from i13c import err
from i13c.graph.nodes import run as run_graph
from tests.semantic import prepare_program


def can_detect_overloaded_symbol_by_arity():
    source, program = prepare_program("""
            asm foo(abc@rax: u32) { }
            fn main() { foo(); }
        """)

    diagnostics = run_graph(program).rule_by_name("e3007")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert source.extract(diagnostic.ref) == b"foo()"


def can_detect_overloaded_symbol_by_range():
    source, program = prepare_program("""
            asm foo(abc@rax: u32[0x01..0x09]) { }
            fn main() { foo(0x10); }
        """)

    diagnostics = run_graph(program).rule_by_name("e3007")

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert source.extract(diagnostic.ref) == b"foo(0x10)"
