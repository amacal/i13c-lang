from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_register_bind():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    id, resolution = resolutions.binds.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target == b"rax"
    assert resolution.accepted[0].mode == "register"

    assert source.extract(resolution.accepted[0].ref) == b"rax"


def can_accept_immediate_bind():
    _, resolutions = prepare_resolutions(
        """
            asm main(v@imm: u16) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    id, resolution = resolutions.binds.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target == b"imm"
    assert resolution.accepted[0].mode == "immediate"


def can_reject_an_unknown_register_bind():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@vax: u16) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    _, resolution = resolutions.binds.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unknown-register"
    assert source.extract(resolution.rejected[0].ref) == b"vax"


def can_detect_a_broken_range_rule_e3013():
    _, rules = prepare_rules(
        """
            asm main(v@vax: u16) { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3013")) == 1
