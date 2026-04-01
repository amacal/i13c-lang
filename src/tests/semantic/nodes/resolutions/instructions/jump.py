from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_syscall_instruction_with_no_operands():
    resolution = prepare_resolution(
        """
            asm main() noreturn { syscall; }
        """
    )

    assert len(resolution.rejected) == 0
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    assert acceptance.mnemonic.name == b"syscall"
    assert len(acceptance.bindings) == 0
    assert len(acceptance.variant) == 0


def can_reject_syscall_instruction_with_unexpected_operand():
    resolution = prepare_resolution(
        """
            asm main() noreturn { syscall rax; }
        """
    )

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1
    rejection = resolution.rejected[0]

    assert rejection.mnemonic.name == b"syscall"
    assert len(rejection.variant) == 0
    assert rejection.reason == b"arity-mismatch"
