from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_valid_immediate():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox rax, 0x1234; }
        """
    )

    assert resolutions.immediates is not None
    assert resolutions.immediates.size() == 1
    id, resolution = resolutions.immediates.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].value.width == 16
    assert resolution.accepted[0].value.data.hex() == "1234"

    assert source.extract(resolution.accepted[0].ref) == b"0x1234"
