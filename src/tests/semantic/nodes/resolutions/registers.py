from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_64bit_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox rax, 0x1234; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    id, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 64

    assert resolution.accepted[0].name == b"rax"
    assert resolution.accepted[0].kind == "64bit"

    assert source.extract(resolution.accepted[0].ref) == b"rax"


def can_accept_32bit_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox eax, 0x1234; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    id, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 32

    assert resolution.accepted[0].name == b"eax"
    assert resolution.accepted[0].kind == "32bit"

    assert source.extract(resolution.accepted[0].ref) == b"eax"


def can_accept_16bit_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox ax, 0x1234; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    id, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 16

    assert resolution.accepted[0].name == b"ax"
    assert resolution.accepted[0].kind == "16bit"

    assert source.extract(resolution.accepted[0].ref) == b"ax"


def can_accept_8bit_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox r8b, 0x12; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    id, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 8

    assert resolution.accepted[0].name == b"r8b"
    assert resolution.accepted[0].kind == "8bit"

    assert source.extract(resolution.accepted[0].ref) == b"r8b"


def can_accept_a_low_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox al, 0x12; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    id, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 8

    assert resolution.accepted[0].name == b"al"
    assert resolution.accepted[0].kind == "low"

    assert source.extract(resolution.accepted[0].ref) == b"al"


def can_accept_a_high_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox ah, 0x12; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    id, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].width == 8

    assert resolution.accepted[0].name == b"ah"
    assert resolution.accepted[0].kind == "high"

    assert source.extract(resolution.accepted[0].ref) == b"ah"


def can_reject_an_unknown_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox sip, 0x1234; }
        """
    )

    assert resolutions.registers is not None
    assert resolutions.registers.size() == 1
    _, resolution = resolutions.registers.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unknown-register"
    assert source.extract(resolution.rejected[0].ref) == b"sip"


def can_detect_a_broken_range_rule_e3017():
    _, rules = prepare_rules(
        """
            asm main() { mox sip, 0x1234; }
        """
    )

    assert len(rules.get("e3017")) == 1
