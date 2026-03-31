from i13c.semantic.typing.entities.operands import Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_bswap_instruction_with_register_operand():
    resolution = prepare_resolution(
        """
            asm main() noreturn { bswap rax; }
        """
    )

    assert len(resolution.rejected) == 0
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"bswap"
    assert len(acceptance.bindings) == 1
    assert len(acceptance.variant) == 1

    assert acceptance.variant == (OperandSpec.registers_64bit(),)

    assert isinstance(acceptance.bindings[0], Register)
