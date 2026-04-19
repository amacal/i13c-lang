from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_valid_parameter_in_a_snippet():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8[0x01..0x02]) { mov rax, rbx; }
        """
    )

    assert resolutions.parameters is not None
    assert resolutions.parameters.size() == 1
    id, resolution = resolutions.parameters.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"v"

    assert resolution.accepted[0].type.name == b"u8"
    assert resolution.accepted[0].type.width == 8

    assert resolution.accepted[0].type.range is not None
    assert resolution.accepted[0].type.range.width == 8

    assert resolution.accepted[0].type.range.lower.width == 8
    assert resolution.accepted[0].type.range.lower.data.hex() == "01"

    assert resolution.accepted[0].type.range.upper.width == 8
    assert resolution.accepted[0].type.range.upper.data.hex() == "02"

    assert source.extract(resolution.accepted[0].ref) == b"v@rax: u8[0x01..0x02]"


def can_accept_valid_parameter_in_a_function():
    source, resolutions = prepare_resolutions(
        """
            fn main(v: u8[0x01..0x02]) { }
        """
    )

    assert resolutions.parameters is not None
    assert resolutions.parameters.size() == 1
    id, resolution = resolutions.parameters.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"v"

    assert resolution.accepted[0].type.name == b"u8"
    assert resolution.accepted[0].type.width == 8

    assert resolution.accepted[0].type.range is not None
    assert resolution.accepted[0].type.range.width == 8

    assert resolution.accepted[0].type.range.lower.width == 8
    assert resolution.accepted[0].type.range.lower.data.hex() == "01"

    assert resolution.accepted[0].type.range.upper.width == 8
    assert resolution.accepted[0].type.range.upper.data.hex() == "02"

    assert source.extract(resolution.accepted[0].ref) == b"v: u8[0x01..0x02]"
