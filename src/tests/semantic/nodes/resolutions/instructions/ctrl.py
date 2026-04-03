from tests.semantic.nodes.resolutions.instructions import prepare_resolution


def can_accept_syscall():
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
