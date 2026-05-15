from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_cpath_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.cpaths is not None
    assert analyses.cpaths.size() == 1
    _, cpaths = analyses.cpaths.peak()

    assert len(cpaths.paths) == 1
    assert cpaths.paths[0][0] == cpaths.flows.source.entry
    assert cpaths.paths[0][1] == cpaths.flows.source.exit


def can_detect_cflow_with_one_callsite():
    _, analyses = prepare_analyses("""
        fn main() { foo(0x42); }
    """)

    assert analyses.cpaths is not None
    assert analyses.cpaths.size() == 1
    _, cpaths = analyses.cpaths.peak()

    assert len(cpaths.paths) == 1
    assert len(cpaths.paths[0]) == 3

    assert cpaths.paths[0][0] == cpaths.flows.source.entry
    assert cpaths.paths[0][2] == cpaths.flows.source.exit

    assert cpaths.paths[0][1] not in (
        cpaths.flows.source.entry,
        cpaths.flows.source.exit,
    )


def can_detect_cpath_with_two_callsites():
    _, analyses = prepare_analyses("""
        fn main() { foo(0x42); bar(0x69); }
    """)

    assert analyses.cpaths is not None
    assert analyses.cpaths.size() == 1

    _, cpaths = analyses.cpaths.peak()

    assert len(cpaths.paths) == 1
    assert len(cpaths.paths[0]) == 4

    assert cpaths.paths[0][0] == cpaths.flows.source.entry
    assert cpaths.paths[0][1] != cpaths.paths[0][2]
    assert cpaths.paths[0][3] == cpaths.flows.source.exit

    assert cpaths.paths[0][1] not in (
        cpaths.flows.source.entry,
        cpaths.flows.source.exit,
    )

    assert cpaths.paths[0][2] not in (
        cpaths.flows.source.entry,
        cpaths.flows.source.exit,
    )
