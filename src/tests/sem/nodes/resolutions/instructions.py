from i13c.sem import model, syntax
from i13c.sem.typing.entities.operands import Immediate, Reference, Register
from i13c.sem.typing.resolutions.instructions import OperandSpec
from tests.sem import prepare_program


def can_do_nothing_without_any_snippet():
    _, program = prepare_program(
        """
            fn main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0


def can_do_nothing_without_any_instruction():
    _, program = prepare_program(
        """
            asm main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0


def can_accept_syscall_instruction_with_no_operands():
    _, program = prepare_program(
        """
            asm main() noreturn { syscall; }
        """
    )

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
    _, program = prepare_program(
        """
            asm main() noreturn { syscall rax; }
        """
    )

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


def can_accept_movregimm_instruction_with_two_operands():
    _, program = prepare_program(
        """
            asm main() noreturn { mov rax, 0x42; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.rejected) == 3
    assert len(value.accepted) == 1
    acceptance = value.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.register(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_reject_movregimm_instruction_with_wrong_arity():
    _, program = prepare_program(
        """
            asm main() noreturn { mov rax; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 4

    for rejection in value.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason == b"wrong-arity"


def can_reject_movregimm_instruction_with_type_mismatch():
    _, program = prepare_program(
        """
            asm main() noreturn { mov 0x42, rax; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 4

    for rejection in value.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason == b"type-mismatch"


def can_accept_movregimm_instruction_with_rewritten_operands():
    _, program = prepare_program(
        """
            asm main(val@imm: u64) noreturn { mov rax, val; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.rejected) == 3
    assert len(value.accepted) == 1
    acceptance = value.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.register(),
        OperandSpec.immediate(64),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Reference)


def can_reject_movregimm_instruction_with_unresolved_operand_reference():
    _, program = prepare_program(
        """
            asm main() noreturn { mov rax, val; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 4

    for rejection in value.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason == b"unresolved"


def can_reject_shlregimm_instruction_with_width_mismatch():
    _, program = prepare_program(
        """
            asm main() noreturn { shl rax, 0x1234; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 1
    rejection = value.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"


def can_reject_shlregimm_instruction_with_unresolved_operand_reference():
    _, program = prepare_program(
        """
            asm main() noreturn { shl rax, shift; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 1
    rejection = value.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"unresolved"


def can_accept_shlregimm_instruction_with_valid_operands():
    _, program = prepare_program(
        """
            asm main() noreturn { shl rax, 0x01; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.rejected) == 0
    assert len(value.accepted) == 1
    acceptance = value.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.register(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_shlregimm_instruction_with_rewritten_operand_reference():
    _, program = prepare_program(
        """
            asm main(val@imm: u8) noreturn { shl rax, val; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.rejected) == 0
    assert len(value.accepted) == 1

    acceptance = value.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.register(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Reference)


def can_reject_shlregimm_instruction_with_rewritten_operand_reference_of_wrong_width():
    _, program = prepare_program(
        """
            asm main(val@imm: u16) noreturn { shl rax, val; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    assert len(value.accepted) == 0
    assert len(value.rejected) == 1
    rejection = value.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"
