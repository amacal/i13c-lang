from i13c.semantic.typing.entities.operands import Immediate, Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_bswap_reg32():
    resolution = prepare_resolution(
        """
            asm main() noreturn { bswap eax; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"bswap"
    assert len(acceptance.bindings) == 1
    assert len(acceptance.variant) == 1

    assert acceptance.variant == (OperandSpec.registers_32bit(),)

    assert isinstance(acceptance.bindings[0], Register)


def can_accept_bswap_reg64():
    resolution = prepare_resolution(
        """
            asm main() noreturn { bswap rax; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"bswap"
    assert len(acceptance.bindings) == 1
    assert len(acceptance.variant) == 1

    assert acceptance.variant == (OperandSpec.registers_64bit(),)

    assert isinstance(acceptance.bindings[0], Register)


def can_reject_bswap_reg16_addr():
    resolution = prepare_resolution(
        """
            asm main() noreturn { bswap ax; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"bswap"
        assert rejection.reason == b"width-mismatch"


def can_reject_bswap_reg8_addr():
    resolution = prepare_resolution(
        """
            asm main() noreturn { bswap al; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1

    for rejection in resolution.rejected:
        assert rejection.mnemonic.name == b"bswap"
        assert rejection.reason == b"width-mismatch"


def can_reject_shl_reg64_imm16():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax, 0x1234; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"


def can_reject_shl_reg64_bl():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax, bl; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"


def can_accept_shl_reg32_imm8():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl eax, 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_32bit(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_shl_reg16_imm8():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl ax, 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_16bit(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_shl_reg8_imm8():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl al, 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_8bit(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_shl_reg64_cl():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax, cl; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.registers_8bit(b"cl"),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Register)
