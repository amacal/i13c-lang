from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_value_declaration():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.values.size() == 0


def can_detect_a_value_declaration_with_literal_initialization():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = 0x12; }
        """
    )

    assert entities.values.size() == 1
    _, value = entities.values.peak()

    assert entities.types.size() == 1
    id, _ = entities.types.peak()

    assert value.name == b"x"
    assert value.type == id

    assert entities.literals.size() == 1
    id, _ = entities.literals.peak()

    assert value.target == id


def can_detect_a_value_declaration_with_expression_initialization():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = abc; }
        """
    )

    assert entities.values.size() == 1
    _, value = entities.values.peak()

    assert entities.types.size() == 1
    id, _ = entities.types.peak()

    assert value.name == b"x"
    assert value.type == id

    assert entities.expressions.size() == 1
    id, _ = entities.expressions.peak()

    assert value.target == id
