from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_statement():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.statements.size() == 0


def can_detect_a_statement_on_assignment():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = 0x12; }
        """
    )

    assert entities.statements.size() == 1
    _, statement = entities.statements.peak()

    assert entities.assigns.size() == 1
    id, _ = entities.assigns.peak()

    assert statement.target == id


def can_detect_a_statement_on_callsite():
    entities = prepare_entities(
        """
            fn main() { foo(bar); }
        """
    )

    assert entities.statements.size() == 1
    _, value = entities.statements.peak()

    assert entities.callsites.size() == 1
    id, _ = entities.callsites.peak()

    assert value.target == id
