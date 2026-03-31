from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.operands import Address, Immediate, Register
from i13c.semantic.typing.resolutions.instructions import (
    InstructionResolution,
    OperandSpec,
    ReferenceToImmediate,
    ReferenceToRegister,
)
from tests.semantic import prepare_program


def prepare_resolution(code: str) -> InstructionResolution:
    _, program = prepare_program(code)
    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    return value


def can_accept_movregimm_instruction_with_two_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, 0x42; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8, 16, 32, 64),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_movregreg_instruction_with_two_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, rbx; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.registers_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Register)


def can_reject_movregreg_instruction_with_reg_mismatch():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, cl; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason in (b"width-mismatch", b"type-mismatch")


def can_reject_movregimm_instruction_with_wrong_arity():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason == b"arity-mismatch"


def can_reject_movregimm_instruction_with_type_mismatch():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov 0x42, rax; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason == b"type-mismatch"


def can_accept_movregimm_instruction_with_rewritten_operands():
    resolution = prepare_resolution(
        """
            asm main(value@imm: u64) noreturn { mov rax, @value; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8, 16, 32, 64),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], ReferenceToImmediate)


def can_reject_movregimm_instruction_with_unresolved_operand_reference():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, @value; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason in (b"unresolved", b"type-mismatch")


def can_accept_movregimm_instruction_with_referenced_register_binding():
    resolution = prepare_resolution(
        """
            asm main(code@rax: u64) noreturn { mov @code, 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8, 16, 32, 64),
    )

    assert isinstance(acceptance.bindings[0], ReferenceToRegister)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_movregimm_instruction_with_narrow_register_binding():
    resolution = prepare_resolution(
        """
            asm main(code@rax: u8) noreturn { mov @code, 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8, 16, 32, 64),
    )

    assert isinstance(acceptance.bindings[0], ReferenceToRegister)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_movoffimm_instruction_without_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax], 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.address_64bit(),
        OperandSpec.immediate(8, 16, 32),
    )

    assert isinstance(acceptance.bindings[0], Address)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_movoffimm_instruction_with_positive_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax + 0x01], 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.address_64bit(),
        OperandSpec.immediate(8, 16, 32),
    )

    assert isinstance(acceptance.bindings[0], Address)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_movoffimm_instruction_with_negative_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax - 0x01], 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.address_64bit(),
        OperandSpec.immediate(8, 16, 32),
    )

    assert isinstance(acceptance.bindings[0], Address)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_movoffreg_instruction_without_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax], rbx; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.address_64bit(),
        OperandSpec.registers_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Address)
    assert isinstance(acceptance.bindings[1], Register)


def can_accept_movoffreg_instruction_with_positive_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax + 0x01], rbx; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.address_64bit(),
        OperandSpec.registers_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Address)
    assert isinstance(acceptance.bindings[1], Register)


def can_accept_movoffreg_instruction_with_negative_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax - 0x01], rbx; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.address_64bit(),
        OperandSpec.registers_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Address)
    assert isinstance(acceptance.bindings[1], Register)


def can_accept_movregoff_instruction_without_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, [rbx]; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_accept_movregoff_instruction_with_positive_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, [rbx + 0x01]; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_accept_movregoff_instruction_with_negative_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, [rbx - 0x01]; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"mov"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)
