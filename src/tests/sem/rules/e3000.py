from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_accept_operands_arity_of_syscall():
    _, program = prepare_program(
        """
            asm main() noreturn {
                syscall;
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_accept_operands_arity_of_mov():
    _, program = prepare_program(
        """
            asm main() noreturn {
                mov rax, 0x1234;
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_detect_invalid_instruction():
    source, program = prepare_program(
        """
            asm main() noreturn {
                xyz;
            }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3000
    assert source.extract(diagnostic.ref) == "xyz"
