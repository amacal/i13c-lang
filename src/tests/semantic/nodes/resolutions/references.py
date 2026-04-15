from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.slots import SlotAcceptance
from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_a_reference_handled_by_a_slot():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u64) { mov rax, @x; }
        """
    )

    assert resolutions.references is not None
    assert resolutions.references.size() == 1
    id, resolution = resolutions.references.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"x"

    assert isinstance(resolution.accepted[0].target, SlotAcceptance)
    assert resolution.accepted[0].target.name == b"x"
    assert resolution.accepted[0].target.bind.mode == "register"
    assert resolution.accepted[0].target.bind.target == b"rax"

    assert source.extract(resolution.accepted[0].ref) == b"@x"


def can_accept_a_reference_handled_by_a_label():
    source, resolutions = prepare_resolutions(
        """
            asm main() { mov rax, rbx; .me: call @me; }
        """
    )

    assert resolutions.references is not None
    assert resolutions.references.size() == 1
    id, resolution = resolutions.references.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].name == b"me"

    assert isinstance(resolution.accepted[0].target, LabelAcceptance)
    assert resolution.accepted[0].target.name == b"me"

    assert source.extract(resolution.accepted[0].ref) == b"@me"


def can_reject_unresolved_reference():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u8, y@rbx: u8) { mov rax, @z; }
        """
    )

    assert resolutions.references is not None
    assert resolutions.references.size() == 1
    _, resolution = resolutions.references.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].name == b"z"
    assert resolution.rejected[0].reason == "unknown-name"

    assert source.extract(resolution.rejected[0].ref) == b"@z"


def can_detect_a_broken_range_rule_e3020():
    _, rules = prepare_rules(
        """
            asm main(x@rax: u8, y@rbx: u8) { mov rax, @z; }
        """
    )

    assert len(rules.get("e3020")) == 1
