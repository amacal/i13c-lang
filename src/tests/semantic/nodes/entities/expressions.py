from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_expression():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.expressions.size() == 0


def can_detect_an_expression_declaration_in_a_value_declaration():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = abc; }
        """
    )

    assert entities.expressions.size() == 1
    _, value = entities.expressions.peak()

    assert value.name == b"abc"


def can_detect_an_expression_in_a_callsite():
    entities = prepare_entities(
        """
            fn main() { abc(cde); }
        """
    )

    assert entities.expressions.size() == 1
    _, value = entities.expressions.peak()

    assert value.name == b"cde"
