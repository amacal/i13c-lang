from tests.semantic.nodes.entities import prepare_entities


def can_handle_no_callsites():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.callsites.size() == 0


def can_detect_a_callsite_with_literal():
    entities = prepare_entities(
        """
            fn main() { foo(0x42); }
        """
    )

    assert entities.callsites.size() == 1
    _, callsites = entities.callsites.peek()

    assert callsites.callee == b"foo"
    assert len(callsites.arguments) == 1

    assert entities.expressions.size() == 1
    id, _ = entities.expressions.peek()

    assert callsites.arguments[0] == id


def can_detect_a_callsite_with_usage():
    entities = prepare_entities(
        """
            fn main(x: u8) { foo(x); }
        """
    )

    assert entities.callsites.size() == 1
    _, callsites = entities.callsites.peek()

    assert callsites.callee == b"foo"
    assert len(callsites.arguments) == 1

    assert entities.expressions.size() == 1
    id, _ = entities.expressions.peek()

    assert callsites.arguments[0] == id
