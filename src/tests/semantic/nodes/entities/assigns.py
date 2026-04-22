from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_value_assignment():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.values.size() == 0


def can_detect_an_assignment_using_the_literal():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = 0x12; }
        """
    )

    assert entities.assigns.size() == 1
    _, assign = entities.assigns.peak()

    assert entities.values.size() == 1
    id, _ = entities.values.peak()

    assert assign.destination == id

    assert entities.literals.size() == 1
    id, _ = entities.literals.peak()

    assert assign.expression == id


def can_detect_an_assignment_using_an_expression():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = abc; }
        """
    )

    assert entities.assigns.size() == 1
    _, assign = entities.assigns.peak()

    assert entities.values.size() == 1
    id, _ = entities.values.peak()

    assert assign.destination == id

    assert entities.expressions.size() == 1
    id, _ = entities.expressions.peak()

    assert assign.expression == id
