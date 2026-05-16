from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_valid_call_of_snippet():
    source, resolutions = prepare_resolutions(
        """
            asm exit() { }
            fn main() { exit(); }
        """
    )

    assert resolutions.calls is not None
    assert resolutions.calls.size() == 1
    id, resolution = resolutions.calls.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.arguments == []

    assert resolution.accepted[0].target.signature.name == b"exit"
    assert resolution.accepted[0].target.signature.parameters == []

    assert source.extract(resolution.accepted[0].ref) == b"exit()"


def can_accept_valid_call_of_other_function():
    source, resolutions = prepare_resolutions(
        """
            fn exit() { }
            fn main() { exit(); }
        """
    )

    assert resolutions.calls is not None
    assert resolutions.calls.size() == 1
    id, resolution = resolutions.calls.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.arguments == []

    assert resolution.accepted[0].target.signature.name == b"exit"
    assert resolution.accepted[0].target.signature.parameters == []

    assert source.extract(resolution.accepted[0].ref) == b"exit()"
