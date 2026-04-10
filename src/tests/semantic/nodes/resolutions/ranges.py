from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_multi_value_range():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8[0x01..0x02]) { mox rax, rbx; }
        """
    )

    assert resolutions.ranges.size() == 1
    id, resolution = resolutions.ranges.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"0x01..0x02"

    assert resolution.accepted[0].lower.width == 8
    assert resolution.accepted[0].lower.data.hex() == "01"

    assert resolution.accepted[0].upper.width == 8
    assert resolution.accepted[0].upper.data.hex() == "02"


def can_accept_single_value_range():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8[0x01..0x01]) { mox rax, rbx; }
        """
    )

    assert resolutions.ranges.size() == 1
    id, resolution = resolutions.ranges.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"0x01..0x01"

    assert resolution.accepted[0].lower.width == 8
    assert resolution.accepted[0].lower.data.hex() == "01"

    assert resolution.accepted[0].upper.width == 8
    assert resolution.accepted[0].upper.data.hex() == "01"


def can_reject_a_range_with_lower_greater_than_upper():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8[0x02..0x01]) { mox rax, rbx; }
        """
    )

    assert resolutions.ranges.size() == 1
    _, resolution = resolutions.ranges.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "lower-greater-than-upper"
    assert source.extract(resolution.rejected[0].ref) == b"0x02..0x01"
