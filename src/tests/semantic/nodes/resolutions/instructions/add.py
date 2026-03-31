from i13c.semantic.typing.entities.operands import Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_add_instruction_with_register_and_imm32_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { add rax, 0x12345678; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"add"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8, 16, 32),
    )

    assert isinstance(acceptance.bindings[0], Register)

def can_reject_add_instruction_with_register_and_imm64_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { add rax, 0x1234567890abcdef; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.reason in (b"width-mismatch", b"type-mismatch")


def can_accept_add_instruction_with_two_register_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { add rax, rbx; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"add"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.registers_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Register)
