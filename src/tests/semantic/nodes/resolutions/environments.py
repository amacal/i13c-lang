from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_a_snippet_environment_without_entries():
    source, resolutions = prepare_resolutions(
        """
            asm main() { }
        """
    )

    assert resolutions.environments is not None
    assert resolutions.environments.size() == 1
    id, resolution = resolutions.environments.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "snippet"
    assert len(resolution.accepted[0].entries) == 0

    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_a_snippet_environment_with_a_label():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mov rax, rbx; .me: nop; }
        """
    )

    assert resolutions.environments is not None
    assert resolutions.environments.size() == 1
    id, resolution = resolutions.environments.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "snippet"
    assert len(resolution.accepted[0].entries) == 1

    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_a_snippet_environment_with_a_slot():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8) { mov rax, rbx; }
        """
    )

    assert resolutions.environments is not None
    assert resolutions.environments.size() == 1
    id, resolution = resolutions.environments.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "snippet"
    assert len(resolution.accepted[0].entries) == 1

    assert source.extract(resolution.accepted[0].ref) == b"main(v@rax: u8)"


def can_reject_duplicate_label_name_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mov rax, rbx; .me: nop; .me: nop; }
        """
    )

    assert resolutions.environments is not None
    assert resolutions.environments.size() == 1
    _, resolution = resolutions.environments.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "duplicated-name"
    assert source.extract(resolution.rejected[0].ref) == b".me:"


def can_reject_duplicate_slot_name_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main(me@rax: u8) { mov rax, rbx; .me: nop; }
        """
    )

    assert resolutions.environments is not None
    assert resolutions.environments.size() == 1
    _, resolution = resolutions.environments.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "duplicated-name"
    assert source.extract(resolution.rejected[0].ref) == b".me:"


def can_detect_a_broken_range_rule_e3019():
    _, rules = prepare_rules(
        """
            asm main() { mov rax, rbx; .me: nop; .me: nop; }
        """
    )

    assert len(rules.get("e3019")) == 1
