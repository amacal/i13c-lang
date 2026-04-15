from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_u8_type_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8) { mov rax, rbx; }
        """
    )

    assert resolutions.types is not None
    assert resolutions.types.size() == 1
    id, resolution = resolutions.types.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 8

    assert resolution.accepted[0].name == b"u8"
    assert resolution.accepted[0].range is None

    assert source.extract(resolution.accepted[0].ref) == b"u8"


def can_accept_u16_with_range():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u16[0x0001..0x0001]) { mov rax, rbx; }
        """
    )

    assert resolutions.types is not None
    assert resolutions.types.size() == 1
    id, resolution = resolutions.types.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 16

    assert resolution.accepted[0].name == b"u16"
    assert resolution.accepted[0].range is not None

    assert source.extract(resolution.accepted[0].ref) == b"u16[0x0001..0x0001]"


def can_reject_an_unknown_type():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: s17) { mov rax, rbx; }
        """
    )

    assert resolutions.types is not None
    assert resolutions.types.size() == 1
    _, resolution = resolutions.types.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unknown-type"
    assert source.extract(resolution.rejected[0].ref) == b"s17"


def can_reject_a_ranged_type_with_incompatible_widths():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8[0x0001..0x0100]) { mov rax, rbx; }
        """
    )

    assert resolutions.types is not None
    assert resolutions.types.size() == 1
    _, resolution = resolutions.types.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "inconsistent-widths"
    assert source.extract(resolution.rejected[0].ref) == b"u8[0x0001..0x0100]"


def can_detect_a_broken_range_rule_e3009():
    _, rules = prepare_rules(
        """
            asm main(v@rax: s17) { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3009")) == 1
