from i13c.semantic import model, syntax
from tests.sem import prepare_program


def can_accept_syscall_instruction_with_no_operands():
    _, program = prepare_program("""
            asm main() noreturn { syscall; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.rejected) == 0
    assert len(value.accepted) == 1
    acceptance = value.accepted[0]

    assert acceptance.mnemonic.name == b"syscall"
    assert len(acceptance.bindings) == 0
    assert len(acceptance.variant) == 0


def can_reject_syscall_instruction_with_unexpected_operand():
    _, program = prepare_program("""
            asm main() noreturn { syscall rax; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 1
    rejection = value.rejected[0]

    assert rejection.mnemonic.name == b"syscall"
    assert len(rejection.variant) == 0
    assert rejection.reason == b"wrong-arity"
