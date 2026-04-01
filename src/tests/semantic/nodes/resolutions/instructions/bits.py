from i13c.semantic.typing.entities.operands import Immediate, Register
from i13c.semantic.typing.resolutions.instructions import (
    OperandSpec,
    ReferenceToImmediate,
)
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_bswap_instruction_with_reg32_operand():
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


def can_accept_bswap_instruction_with_reg64_operand():
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


def can_reject_shlregimm_instruction_with_arity_mismatch():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"arity-mismatch"


def can_reject_shlregimm_instruction_with_width_mismatch():
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


def can_reject_shlregimm_instruction_with_unresolved_operand_reference():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax, @shift; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"unresolved"


def can_accept_shlregimm_instruction_with_valid_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax, 0x01; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Immediate)


def can_accept_shlregimm_instruction_with_rewritten_operand_reference():
    resolution = prepare_resolution(
        """
            asm main(value@imm: u8) noreturn { shl rax, @value; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1

    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], ReferenceToImmediate)


def can_reject_shlregimm_instruction_with_rewritten_operand_reference_of_wrong_width():
    resolution = prepare_resolution(
        """
            asm main(value@imm: u16) noreturn { shl rax, @value; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"


def can_reject_shlregimm_instruction_with_immediate_out_of_range():
    resolution = prepare_resolution(
        """
            asm main() noreturn { shl rax, 0x0142; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"


def can_reject_shlregimm_instruction_with_reference_out_of_range():
    resolution = prepare_resolution(
        """
            asm main(value@imm: u16) noreturn { shl rax, @value; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) >= 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"shl"
    assert rejection.reason == b"width-mismatch"


def can_accept_shlregimm_instruction_with_reference_within_range():
    resolution = prepare_resolution(
        """
            asm main(value@imm: u16[0x00..0xff]) noreturn { shl rax, @value; }
        """
    )

    assert len(resolution.rejected) >= 1
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"shl"
    assert len(acceptance.variant) == 2

    assert acceptance.variant == (
        OperandSpec.registers_64bit(),
        OperandSpec.immediate(8),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], ReferenceToImmediate)


def can_accept_shlregreg_instruction_with_cl_as_second_operand():
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
        OperandSpec.registers_8bit(),
    )

    assert isinstance(acceptance.bindings[0], Register)
    assert isinstance(acceptance.bindings[1], Register)
