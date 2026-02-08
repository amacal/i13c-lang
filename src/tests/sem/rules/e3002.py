from i13c import err, semantic
from i13c.semantic.model import build_semantic_graph
from i13c.semantic.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_invalid_operand_types_of_mov():
    source, program = prepare_program("""
            asm main() noreturn {
                mov 0x1234, 0x5678;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3002.validate_assembly_operand_types(model)

    assert len(diagnostics) == 4

    # all of them are related to E3002
    for diagnostic in diagnostics:
        assert diagnostic.code == err.ERROR_3002
        assert source.extract(diagnostic.ref) == b"mov 0x1234, 0x5678;"


def can_detect_invalid_operand_types_of_shl():
    source, program = prepare_program("""
            asm main() noreturn {
                shl rax, rbx;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3002.validate_assembly_operand_types(model)

    assert len(diagnostics) == 1

    assert diagnostics[0].code == err.ERROR_3002
    assert source.extract(diagnostics[0].ref) == b"shl rax, rbx;"


def can_accept_valid_operand_type_of_shl_reg64_imm8():
    _, program = prepare_program("""
            asm main() noreturn {
                shl rax, 0x08;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3002.validate_assembly_operand_types(model)

    assert len(diagnostics) == 0


def can_accept_valid_operand_type_of_shl_reg64_imm8_via_parameters():
    _, program = prepare_program("""
            asm main(count@imm: u8) noreturn {
                shl rax, count;
            }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3002.validate_assembly_operand_types(model)

    assert len(diagnostics) == 0
