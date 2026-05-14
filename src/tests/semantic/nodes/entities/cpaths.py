from tests.semantic.nodes.entities import prepare_entities


def can_detect_cpath_in_empty_function():
    entities = prepare_entities("""
        fn main() { }
    """)

    assert entities.cpaths is not None
    assert entities.cpaths.size() == 1
    _, cpaths = entities.cpaths.peak()

    assert len(cpaths.paths) == 1
    assert cpaths.paths[0][0] == cpaths.flows.source.entry
    assert cpaths.paths[0][1] == cpaths.flows.source.exit


def can_detect_cflow_with_one_callsite():
    entities = prepare_entities("""
        fn main() { foo(0x42); }
    """)

    assert entities.cpaths is not None
    assert entities.cpaths.size() == 1
    _, cpaths = entities.cpaths.peak()

    assert len(cpaths.paths) == 1
    assert len(cpaths.paths[0]) == 3

    assert cpaths.paths[0][0] == cpaths.flows.source.entry
    assert cpaths.paths[0][2] == cpaths.flows.source.exit

    assert cpaths.paths[0][1] not in (
        cpaths.flows.source.entry,
        cpaths.flows.source.exit,
    )


def can_detect_cpath_with_two_callsites():
    entities = prepare_entities("""
        fn main() { foo(0x42); bar(0x69); }
    """)

    assert entities.cpaths is not None
    assert entities.cpaths.size() == 1

    _, cpaths = entities.cpaths.peak()

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
