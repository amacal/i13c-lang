from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_a_snippet_flags_noreturn():
    source, resolutions = prepare_resolutions(
        """
            asm main() noreturn { mov rax, rbx; }
        """
    )

    assert resolutions.flags is not None
    assert resolutions.flags.size() == 1
    id, resolution = resolutions.flags.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].noreturn
    assert len(resolution.accepted[0].clobbers) == 0

    assert source.extract(resolution.accepted[0].ref) == b"noreturn"


def can_accept_a_snippet_flags_clobbers():
    source, resolutions = prepare_resolutions(
        """
            asm main() clobbers rax, rbx { mov rax, rbx; }
        """
    )

    assert resolutions.flags is not None
    assert resolutions.flags.size() == 1
    id, resolution = resolutions.flags.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].noreturn is False

    assert len(resolution.accepted[0].clobbers) == 2
    assert resolution.accepted[0].clobbers[0].name == b"rax"
    assert resolution.accepted[0].clobbers[1].name == b"rbx"

    assert source.extract(resolution.accepted[0].ref) == b"clobbers rax, rbx"


def can_reject_duplicate_clobber_name_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main() clobbers rax, rax { mov rax, rbx; }
        """
    )

    assert resolutions.flags is not None
    assert resolutions.flags.size() == 1
    _, resolution = resolutions.flags.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "duplicated-register"
    assert source.extract(resolution.rejected[0].ref) == b"rax"


def can_detect_a_duplicate_clobber_name_usage():
    _, rules = prepare_rules(
        """
            asm main() clobbers rax, rax { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3002")) == 1
