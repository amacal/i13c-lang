from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_valid_assign_from_literal():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u16 = 0x1234; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].destination.name == b"x"

    assert resolution.accepted[0].destination.type.width == 16
    assert resolution.accepted[0].destination.type.range is None

    assert resolutions.literals is not None
    assert resolutions.literals.size() == 1
    id, _ = resolutions.literals.peak()

    assert resolution.accepted[0].expression == id
    assert source.extract(resolution.accepted[0].ref) == b"x: u16 = 0x1234"


def can_accept_valid_assign_from_parameter():
    source, resolutions = prepare_resolutions(
        """
            fn main(v: u16) { val x: u16 = v; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].destination.name == b"x"

    assert resolution.accepted[0].destination.type.width == 16
    assert resolution.accepted[0].destination.type.range is None

    assert source.extract(resolution.accepted[0].ref) == b"x: u16 = v"
