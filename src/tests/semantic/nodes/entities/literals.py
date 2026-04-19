from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_literal():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.literals.size() == 0


def can_detect_a_literal_in_a_function():
    entities = prepare_entities(
        """
            fn main() { val x: u16 = 0x1234; }
        """
    )

    assert entities.literals.size() == 1
    _, value = entities.literals.peak()

    assert value.target.width == 16
    assert value.target.data.hex() == "1234"
