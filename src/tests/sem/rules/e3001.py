from i13c import err
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_accept_default_snippet_type_ranges():
    _, program = prepare_program("""
        asm main(value@rax: u64) { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 0


def can_accept_default_function_type_ranges():
    _, program = prepare_program("""
        fn main(value: u64) { exit(); }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 0


def can_accept_custom_snippet_type_ranges():
    _, program = prepare_program("""
        asm main(value@rax: u64[0x00..0xff]) { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 0


def can_accept_custom_function_type_ranges():
    _, program = prepare_program("""
        fn main(value: u64[0x00..0xff]) { exit(); }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 0


def can_accept_equal_snippet_type_ranges():
    _, program = prepare_program("""
        asm main(value@rax: u64[0x42..0x42]) { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 0


def can_accept_equal_function_type_ranges():
    _, program = prepare_program("""
        fn main(value: u64[0x42..0x42]) { exit(); }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 0


def can_reject_invalid_snippet_type_ranges():
    source, program = prepare_program("""
        asm main(value@rax: u64[0xff..0x00]) { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(value@rax: u64[0xff..0x00])"


def can_reject_invalid_function_type_ranges():
    source, program = prepare_program("""
        fn main(value: u64[0xff..0x00]) { exit(); }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(value: u64[0xff..0x00])"


def can_reject_invalid_snippet_ranges_out_of_type_ranges():
    source, program = prepare_program("""
        asm main(value@rax: u8[0x000..0x200]) { syscall; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(value@rax: u8[0x000..0x200])"


def can_reject_invalid_function_ranges_out_of_type_ranges():
    source, program = prepare_program("""
        fn main(value: u8[0x000..0x200]) { exit(); }
    """)

    diagnostics = run_graph(program).rule_by_name("e3001")

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(value: u8[0x000..0x200])"
