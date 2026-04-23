from tests.semantic.nodes.resolutions import prepare_resolutions


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
    assert resolution.accepted[0].binding is not None
    assert resolution.accepted[0].binding.owner == id

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
    assert resolution.accepted[0].binding is not None

    assert resolution.accepted[0].binding.owner == id
    assert len(resolution.accepted[0].binding.binds) == 1

    assert resolution.accepted[0].binding.binds[0].src == b"x"
    assert resolution.accepted[0].binding.binds[0].dst == b"rbx"

    assert resolutions.instructions is not None
    id, _ = resolutions.instructions.peak()

    assert resolution.accepted[0].instructions[0].id == id
    assert source.extract(resolution.accepted[0].ref) == b"main(x@rbx: u8)"
