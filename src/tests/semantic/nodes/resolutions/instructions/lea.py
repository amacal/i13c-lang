from i13c.semantic.typing.entities.operands import Address, Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_lea_instruction_with_address_without_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea rax, [rbx]; }
        """
    )

    assert len(resolution.rejected) == 0
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"lea"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_accept_lea_instruction_with_address_with_positive_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea rax, [rbx + 0x1234]; }
        """
    )

    assert len(resolution.rejected) == 0
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"lea"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_accept_lea_instruction_with_address_with_negative_offset():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea rax, [rbx - 0x1234]; }
        """
    )

    assert len(resolution.rejected) == 0
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"lea"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)
