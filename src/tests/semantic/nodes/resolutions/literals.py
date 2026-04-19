from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_valid_literal():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u16 = 0x1234; }
        """
    )

    assert resolutions.literals is not None
    assert resolutions.literals.size() == 1
    id, resolution = resolutions.literals.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.width == 16
    assert resolution.accepted[0].target.data.hex() == "1234"

    assert source.extract(resolution.accepted[0].ref) == b"0x1234"
