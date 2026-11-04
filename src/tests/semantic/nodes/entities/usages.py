from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_usage():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.usages.size() == 0


def can_detect_an_usage_declaration_in_a_value_declaration():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = abc; }
        """
    )

    assert entities.usages.size() == 1
    _, value = entities.usages.peek()

    assert value.name == b"abc"


def can_detect_an_usage_in_a_callsite():
    entities = prepare_entities(
        """
            fn main() { abc(cde); }
        """
    )

    assert entities.usages.size() == 1
    _, value = entities.usages.peek()

    assert value.name == b"cde"
