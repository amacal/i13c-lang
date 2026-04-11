from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_a_snippet_signature_without_slots():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mox rax, rbx; }
        """
    )

    assert resolutions.signatures is not None
    assert resolutions.signatures.size() == 1
    id, resolution = resolutions.signatures.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"main"
    assert len(resolution.accepted[0].slots) == 0

    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_a_snippet_signature_with_a_slot():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u16[0x0001..0x0001]) { mox rax, rbx; }
        """
    )

    assert resolutions.signatures is not None
    assert resolutions.signatures.size() == 1
    id, resolution = resolutions.signatures.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id

    assert resolution.accepted[0].name == b"main"
    assert len(resolution.accepted[0].slots) == 1

    assert resolution.accepted[0].slots[0].name == b"v"
    assert resolution.accepted[0].slots[0].bind.mode == "register"
    assert resolution.accepted[0].slots[0].bind.target == b"rax"

    assert (
        source.extract(resolution.accepted[0].ref)
        == b"main(v@rax: u16[0x0001..0x0001])"
    )


def can_reject_duplicate_slot_name_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u8, x@rbx: u8) { mox rax, rbx; }
        """
    )

    assert resolutions.signatures is not None
    assert resolutions.signatures.size() == 1
    _, resolution = resolutions.signatures.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "duplicated-name"
    assert source.extract(resolution.rejected[0].ref) == b"x@rbx: u8"


def can_reject_duplicated_slot_bind_usage():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u8, y@rax: u8) { mox rax, rbx; }
        """
    )

    assert resolutions.signatures is not None
    assert resolutions.signatures.size() == 1
    _, resolution = resolutions.signatures.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "duplicated-register"
    assert source.extract(resolution.rejected[0].ref) == b"y@rax: u8"


def can_detect_a_broken_range_rule_e3003():
    _, rules = prepare_rules(
        """
            asm main(x@rax: u8, x@rbx: u8) { mox rax, rbx; }
        """
    )

    assert len(rules.get("e3003")) == 1


def can_detect_a_broken_range_rule_e3015():
    _, rules = prepare_rules(
        """
            asm main(x@rax: u8, y@rax: u8) { mox rax, rbx; }
        """
    )

    assert len(rules.get("e3015")) == 1
