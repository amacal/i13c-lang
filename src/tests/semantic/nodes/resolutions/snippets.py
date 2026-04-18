from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_a_snippet():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mov rax, rbx; }
        """
    )

    assert resolutions.snippets is not None
    assert resolutions.snippets.size() == 1
    id, resolution = resolutions.snippets.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert len(resolution.accepted[0].instructions) == 1

    assert resolutions.signatures is not None
    id, _ = resolutions.signatures.peak()

    assert resolution.accepted[0].signature.id == id

    assert resolutions.instructions is not None
    id, _ = resolutions.instructions.peak()

    assert resolution.accepted[0].instructions[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_reject_duplicated_slot_bind_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u8, y@rax: u8) { mov rax, rbx; }
        """
    )

    assert resolutions.snippets is not None
    assert resolutions.snippets.size() == 1
    _, resolution = resolutions.snippets.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "duplicated-binds"
    assert source.extract(resolution.rejected[0].ref) == b"rax"


def can_detect_a_broken_range_rule_e3015():
    _, rules = prepare_rules(
        """
            asm main(x@rax: u8, y@rax: u8) { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3015")) == 1
