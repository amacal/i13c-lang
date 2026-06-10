from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_a_function():
    _, resolutions = prepare_resolutions(
        """
            fn main() { }
        """
    )

    assert resolutions.functions is not None
    assert resolutions.functions.size() == 1
    id, resolution = resolutions.functions.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id

    assert resolutions.signatures is not None
    id, _ = resolutions.signatures.peak()

    assert resolution.accepted[0].signature.id == id
    assert resolution.accepted[0].noreturn is False


def can_accept_a_snippet_with_parameters():
    _, resolutions = prepare_resolutions(
        """
            fn main(x: u8) { }
        """
    )

    assert resolutions.functions is not None
    assert resolutions.functions.size() == 1
    id, resolution = resolutions.functions.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolutions.signatures is not None
    id, _ = resolutions.signatures.peak()

    assert resolution.accepted[0].signature.id == id


def can_accept_a_function_with_noreturn():
    _, resolutions = prepare_resolutions(
        """
            asm exit() noreturn { }
            fn main() noreturn { exit(); }
        """
    )

    assert resolutions.functions is not None
    assert resolutions.functions.size() == 1
    id, resolution = resolutions.functions.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].noreturn is True
