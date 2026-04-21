from tests.semantic.nodes.resolutions import prepare_resolutions


def can_accept_an_empty_function():
    source, resolutions = prepare_resolutions(
        """
            fn main() { }
        """
    )

    assert resolutions.cflows is not None
    assert resolutions.cflows.size() == 1
    id, resolution = resolutions.cflows.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert len(resolution.accepted[0].environments) == 2

    entry = resolution.accepted[0].entry
    assert len(resolution.accepted[0].environments[entry]) == 0

    exit = resolution.accepted[0].exit
    assert len(resolution.accepted[0].environments[exit]) == 0

    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_an_empty_function_with_parameters():
    source, resolutions = prepare_resolutions(
        """
            fn main(x: u32, y: u32) { }
        """
    )

    assert resolutions.cflows is not None
    assert resolutions.cflows.size() == 1
    id, resolution = resolutions.cflows.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert len(resolution.accepted[0].environments) == 2

    entry = resolution.accepted[0].entry
    assert len(resolution.accepted[0].environments[entry]) == 0

    exit = resolution.accepted[0].exit
    assert len(resolution.accepted[0].environments[exit]) == 2

    assert b"x" in resolution.accepted[0].environments[exit]
    assert b"y" in resolution.accepted[0].environments[exit]

    assert source.extract(resolution.accepted[0].ref) == b"main(x: u32, y: u32)"


def can_accept_a_function_with_declared_value():
    source, resolutions = prepare_resolutions(
        """
            fn main() {
                val y: u32 = 0x01234567;
            }
        """
    )

    assert resolutions.cflows is not None
    assert resolutions.cflows.size() == 1
    id, resolution = resolutions.cflows.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert len(resolution.accepted[0].environments) == 3

    entry = resolution.accepted[0].entry
    assert len(resolution.accepted[0].environments[entry]) == 0

    exit = resolution.accepted[0].exit
    assert len(resolution.accepted[0].environments[exit]) == 1

    assert b"y" in resolution.accepted[0].environments[exit]

    assert source.extract(resolution.accepted[0].ref) == b"main()"


def can_accept_a_function_with_parameters_and_values():
    source, resolutions = prepare_resolutions(
        """
            fn main(x: u32, y: u32) {
                val a: u32 = 0x01234567;
                val b: u32 = y;
            }
        """
    )

    assert resolutions.cflows is not None
    assert resolutions.cflows.size() == 1
    id, resolution = resolutions.cflows.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert len(resolution.accepted[0].environments) == 4

    entry = resolution.accepted[0].entry
    assert len(resolution.accepted[0].environments[entry]) == 0

    exit = resolution.accepted[0].exit
    assert len(resolution.accepted[0].environments[exit]) == 4

    assert b"x" in resolution.accepted[0].environments[exit]
    assert b"y" in resolution.accepted[0].environments[exit]

    assert b"a" in resolution.accepted[0].environments[exit]
    assert b"b" in resolution.accepted[0].environments[exit]

    assert source.extract(resolution.accepted[0].ref) == b"main(x: u32, y: u32)"
