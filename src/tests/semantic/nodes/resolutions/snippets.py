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
    assert resolution.accepted[0].binding.owner == id

    assert resolution.accepted[0].noreturn is False
    assert len(resolution.accepted[0].clobbers) == 0

    assert resolutions.instructions is not None
    id, _ = resolutions.instructions.peak()

    assert resolution.accepted[0].instructions[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_a_snippet_with_parameters():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rbx: u8) { mov rax, rbx; }
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
    assert resolution.accepted[0].binding.owner == id
    assert len(resolution.accepted[0].binding.binds) == 1

    assert resolution.accepted[0].binding.binds[0].src == b"x"
    assert resolution.accepted[0].binding.binds[0].dst == b"rbx"

    assert resolutions.instructions is not None
    id, _ = resolutions.instructions.peak()

    assert resolution.accepted[0].instructions[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"main(x@rbx: u8)"


def can_accept_a_snippet_with_noreturn():
    source, resolutions = prepare_resolutions(
        """
            asm main() noreturn { mov rax, rbx; }
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
    assert resolution.accepted[0].binding.owner == id

    assert resolution.accepted[0].noreturn is True
    assert len(resolution.accepted[0].clobbers) == 0

    assert resolutions.instructions is not None
    id, _ = resolutions.instructions.peak()

    assert resolution.accepted[0].instructions[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_a_snippet_with_clobbers():
    source, resolutions = prepare_resolutions(
        """
            asm main() clobbers rax, rbx { mov rax, rbx; }
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
    assert resolution.accepted[0].binding.owner == id

    assert resolution.accepted[0].noreturn is False
    assert len(resolution.accepted[0].clobbers) == 2

    assert resolution.accepted[0].clobbers[0].name == b"rax"
    assert resolution.accepted[0].clobbers[1].name == b"rbx"

    assert resolutions.instructions is not None
    id, _ = resolutions.instructions.peak()

    assert resolution.accepted[0].instructions[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_reject_a_snippet_with_rsp_in_clobbers():
    source, resolutions = prepare_resolutions(
        """
            asm main() clobbers rsp { mov rax, rbx; }
        """
    )

    assert resolutions.snippets is not None
    assert resolutions.snippets.size() == 1
    _, resolution = resolutions.snippets.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unallowed-clobber"
    assert source.extract(resolution.rejected[0].ref) == b"main()"


def can_reject_a_snippet_with_rip_in_clobbers():
    source, resolutions = prepare_resolutions(
        """
            asm main() clobbers rip { mov rax, rbx; }
        """
    )

    assert resolutions.snippets is not None
    assert resolutions.snippets.size() == 1
    _, resolution = resolutions.snippets.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unallowed-clobber"
    assert source.extract(resolution.rejected[0].ref) == b"main()"


def can_reject_a_snippet_with_non_64_in_clobbers():
    source, resolutions = prepare_resolutions(
        """
            asm main() clobbers r8d { mov rax, rbx; }
        """
    )

    assert resolutions.snippets is not None
    assert resolutions.snippets.size() == 1
    _, resolution = resolutions.snippets.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unallowed-clobber"
    assert source.extract(resolution.rejected[0].ref) == b"main()"


def can_detect_a_broken_range_rule_e3015():
    _, rules = prepare_rules(
        """
            asm main() clobbers rsp { mov rax, rbx; }
        """
    )

    assert len(rules.get("e3015")) == 1
