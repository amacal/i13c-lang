from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_register_bind():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rax: u8) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    id, resolution = resolutions.binds.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].src == b"v"
    assert resolution.accepted[0].dst == b"rax"
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
    id, resolution = resolutions.binds.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].src == b"v"
    assert resolution.accepted[0].dst == b"imm"
    assert resolution.accepted[0].mode == "immediate"


def can_reject_an_unknown_register_bind():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@vax: u16) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    _, resolution = resolutions.binds.peek()

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


def can_accept_a_result_bind():
    source, resolutions = prepare_resolutions(
        """
            asm main() -> u64@rdx { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    id, resolution = resolutions.binds.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].src == b"_ret"
    assert resolution.accepted[0].dst == b"rdx"
    assert resolution.accepted[0].mode == "register"

    assert source.extract(resolution.accepted[0].ref) == b"rdx"


def can_reject_a_result_bind_to_r11():
    source, resolutions = prepare_resolutions(
        """
            asm main() -> u64@r11 { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    _, resolution = resolutions.binds.peek()

    # r11 is the scratch register used to move the result after the call
    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert source.extract(resolution.rejected[0].ref) == b"r11"


def can_detect_a_result_bind_to_r11_rule_e3013():
    _, rules = prepare_rules(
        """
            asm main() -> u64@r11 { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3013")) == 1


def can_reject_a_result_bind_to_rsp():
    source, resolutions = prepare_resolutions(
        """
            asm main() -> u64@rsp { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    _, resolution = resolutions.binds.peek()

    # rsp is the stack pointer, used by the call itself and the spill slots
    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert source.extract(resolution.rejected[0].ref) == b"rsp"


def can_detect_a_result_bind_to_rsp_rule_e3013():
    _, rules = prepare_rules(
        """
            asm main() -> u64@rsp { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3013")) == 1


def can_reject_a_parameter_bind_to_r11():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@r11: u64) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    _, resolution = resolutions.binds.peek()

    # r11 is the scratch register used to move arguments before the call
    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "incorrect-register"
    assert source.extract(resolution.rejected[0].ref) == b"r11"


def can_reject_a_parameter_bind_to_rsp():
    source, resolutions = prepare_resolutions(
        """
            asm main(v@rsp: u64) { mov rax, rbx; }
        """
    )

    assert resolutions.binds is not None
    assert resolutions.binds.size() == 1
    _, resolution = resolutions.binds.peek()

    # rsp is the stack pointer, it can't carry an argument
    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "incorrect-register"
    assert source.extract(resolution.rejected[0].ref) == b"rsp"


def can_detect_a_parameter_bind_to_r11_rule_e3013():
    _, rules = prepare_rules(
        """
            asm main(v@r11: u64) { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3013")) == 1
