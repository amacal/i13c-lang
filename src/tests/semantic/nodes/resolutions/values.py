from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_valid_value():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u16 = 0x1234; }
        """
    )

    assert resolutions.values is not None
    assert resolutions.values.size() == 1
    id, resolution = resolutions.values.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"x"

    assert resolution.accepted[0].type.width == 16
    assert resolution.accepted[0].type.range is None

    assert source.extract(resolution.accepted[0].ref) == b"x: u16"
