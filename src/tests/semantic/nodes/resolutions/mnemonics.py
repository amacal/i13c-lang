from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_a_known_mnemonic():
    source, resolutions = prepare_resolutions(
        """
            asm main() { bswap rax; }
        """
    )

    assert resolutions.mnemonics is not None
    assert resolutions.mnemonics.size() == 1
    id, resolution = resolutions.mnemonics.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"bswap"
    assert len(resolution.accepted[0].variants) == 2

    assert source.extract(resolution.accepted[0].ref) == b"bswap"


def can_reject_an_unknown_mnemonic():
    source, resolutions = prepare_resolutions(
        """
            asm main() { strange rax; }
        """
    )

    assert resolutions.mnemonics is not None
    assert resolutions.mnemonics.size() == 1
    _, resolution = resolutions.mnemonics.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unknown-mnemonic"
    assert source.extract(resolution.rejected[0].ref) == b"strange"
