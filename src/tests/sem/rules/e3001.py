from i13c import err, semantic
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_accept_default_snippet_type_ranges():
    _, program = prepare_program("""
        asm main(val@rax: u64) { syscall; }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 0


def can_accept_default_function_type_ranges():
    _, program = prepare_program("""
        fn main(val: u64) { exit(); }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 0


def can_accept_custom_snippet_type_ranges():
    _, program = prepare_program("""
        asm main(val@rax: u64[0x00..0xff]) { syscall; }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 0


def can_accept_custom_function_type_ranges():
    _, program = prepare_program("""
        fn main(val: u64[0x00..0xff]) { exit(); }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 0


def can_accept_equal_snippet_type_ranges():
    _, program = prepare_program("""
        asm main(val@rax: u64[0x42..0x42]) { syscall; }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 0


def can_accept_equal_function_type_ranges():
    _, program = prepare_program("""
        fn main(val: u64[0x42..0x42]) { exit(); }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 0


def can_reject_invalid_snippet_type_ranges():
    source, program = prepare_program("""
        asm main(val@rax: u64[0xff..0x00]) { syscall; }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(val@rax: u64[0xff..0x00])"


def can_reject_invalid_function_type_ranges():
    source, program = prepare_program("""
        fn main(val: u64[0xff..0x00]) { exit(); }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(val: u64[0xff..0x00])"


def can_reject_invalid_snippet_ranges_out_of_type_ranges():
    source, program = prepare_program("""
        asm main(val@rax: u8[0x000..0x200]) { syscall; }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(val@rax: u8[0x000..0x200])"


def can_reject_invalid_function_ranges_out_of_type_ranges():
    source, program = prepare_program("""
        fn main(val: u8[0x000..0x200]) { exit(); }
    """)

    model = run_graph(program).semantic_graph()
    diagnostics = semantic.e3001.validate_type_ranges(model)

    assert len(diagnostics) == 1
    assert diagnostics[0].code == err.ERROR_3001
    assert source.extract(diagnostics[0].ref) == b"main(val: u8[0x000..0x200])"
