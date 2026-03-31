from i13c.semantic.typing.entities.operands import Register
from i13c.semantic.typing.resolutions.instructions import OperandSpec
from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_add_instruction_with_two_register_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { add rax, rbx; }
        """
    )

    assert len(resolution.rejected) == 0
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
