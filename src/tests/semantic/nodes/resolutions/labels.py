from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_a_label():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mov rax, rbx; .me: nop; }
        """
    )

    assert resolutions.labels is not None
    assert resolutions.labels.size() == 1
    id, resolution = resolutions.labels.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"me"

    assert source.extract(resolution.accepted[0].ref) == b".me:"
