from i13c.graph.nodes import run as run_graph
from tests.semantic import prepare_program


def can_detect_invalid_operand_types_of_mov():
    source, program = prepare_program("""
        asm main() noreturn { mov 0x1234, 0x5678; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3002")

    assert len(diagnostics) >= 1

    # all of them are related to E3002
    for diagnostic in diagnostics:
        assert diagnostic.code == "E3002"
        assert source.extract(diagnostic.ref) == b"mov 0x1234, 0x5678;"


def can_detect_invalid_operand_types_of_shl():
    source, program = prepare_program("""
        asm main() noreturn { shl rax, rbx; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3002")

    assert len(diagnostics) >= 1

    assert diagnostics[0].code == "E3002"
    assert source.extract(diagnostics[0].ref) == b"shl rax, rbx;"


def can_accept_valid_operand_type_of_shl_reg64_imm8():
    _, program = prepare_program("""
        asm main() noreturn { shl rax, 0x08; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3002")

    assert len(diagnostics) == 0


def can_accept_valid_operand_type_of_shl_reg64_imm8_via_parameters():
    _, program = prepare_program("""
        asm main(count@imm: u8) noreturn { shl rax, @count; }
    """)

    diagnostics = run_graph(program).rule_by_name("e3002")

    assert len(diagnostics) == 0
