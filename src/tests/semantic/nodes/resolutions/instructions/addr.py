from i13c.semantic.typing.entities.operands import Address, Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_lea_reg64_addr_disp0():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea rax, [rbx]; }
        """
    )

    assert len(resolution.rejected) >= 1
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


def can_accept_lea_reg64_addr_with_positive_disp32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea rax, [rbx + 0x1234]; }
        """
    )

    assert len(resolution.rejected) >= 1
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


def can_accept_lea_reg64_addr_with_negative_disp32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea rax, [rbx - 0x1234]; }
        """
    )

    assert len(resolution.rejected) >= 1
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


def can_accept_lea_reg32_addr_disp0():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea eax, [rbx]; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"lea"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_32bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_accept_lea_reg32_addr_with_positive_disp32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea eax, [rbx + 0x1234]; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"lea"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_32bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_accept_lea_reg32_addr_with_negative_disp32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea eax, [rbx - 0x1234]; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"lea"
    assert len(acceptance.bindings) == 2
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_32bit(),
        OperandSpec.address_64bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Address)


def can_reject_lea_reg16_addr():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea ax, [rbx]; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"lea"
        assert rejection.reason == b"width-mismatch"


def can_reject_lea_reg8_addr():
    resolution = prepare_resolution(
        """
            asm main() noreturn { lea al, [rbx]; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"lea"
        assert rejection.reason == b"width-mismatch"
