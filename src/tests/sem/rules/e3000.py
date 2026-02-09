from i13c import err, semantic
from i13c.graph.nodes import run as run_graph
from tests.sem import prepare_program


def can_accept_operands_arity_of_syscall():
    _, program = prepare_program("""
            asm main() noreturn {
                syscall;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_accept_operands_arity_of_mov():
    _, program = prepare_program("""
            asm main() noreturn {
                mov rax, 0x1234;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_accept_shl_reg64_imm8_with_0x01():
    _, program = prepare_program("""
            asm main() noreturn {
                shl rax, 0x01;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_accept_shl_reg64_imm8_with_0x41():
    _, program = prepare_program("""
            asm main() noreturn {
                shl rax, 0x41;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_detect_invalid_instruction():
    source, program = prepare_program("""
            asm main() noreturn {
                xyz;
            }
        """)

    model = run_graph(program)
    diagnostics = semantic.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3000
    assert source.extract(diagnostic.ref) == b"xyz;"
