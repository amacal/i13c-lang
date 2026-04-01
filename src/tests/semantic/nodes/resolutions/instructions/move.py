from i13c.semantic.typing.entities.operands import Address, Immediate, Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_mov_reg64_imm8():
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


def can_accept_mov_reg64_imm16():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, 0x1234; }
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


def can_accept_mov_reg64_imm32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, 0x12345678; }
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


def can_accept_mov_reg64_imm64():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov rax, 0x1234567890abcdef; }
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


def can_accept_mov_reg64_reg64():
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


def can_reject_mov_reg64_reg8():
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


def can_reject_mov_imm8_reg64():
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



def can_accept_mov_addr_imm8():
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


def can_accept_mov_addr_imm16():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax], 0x1234; }
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


def can_accept_mov_addr_imm32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax], 0x12345678; }
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


def can_reject_mov_addr_imm64():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax], 0x1234567890abcdef; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason in (b"width-mismatch", b"type-mismatch")



def can_accept_mov_addr_imm8_with_positive_disp8():
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


def can_accept_mov_addr_imm8_with_negative_disp8():
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


def can_accept_mov_addr_reg64():
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


def can_accept_mov_addr_reg64_with_positive_disp8():
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


def can_accept_mov_addr_reg64_with_negative_disp8():
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


def can_accept_mov_reg64_addr():
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


def can_accept_mov_reg64_addr_with_positive_disp8():
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


def can_accept_mov_reg64_addr_with_negative_disp8():
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


def can_reject_mov_addr_addr():
    resolution = prepare_resolution(
        """
            asm main() noreturn { mov [rax], [rbx]; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"mov"
        assert rejection.reason == b"type-mismatch"
