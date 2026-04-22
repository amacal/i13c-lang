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
    _, callsites = entities.callsites.peak()

    assert callsites.callee == b"foo"
    assert len(callsites.arguments) == 1

    assert entities.literals.size() == 1
    id, _ = entities.literals.peak()

    assert callsites.arguments[0] == id


def can_detect_a_callsite_with_expression():
    entities = prepare_entities(
        """
            fn main() { val x: u8 = 0x42; foo(x); }
        """
    )

    assert entities.callsites.size() == 1
    _, callsites = entities.callsites.peak()

    assert callsites.callee == b"foo"
    assert len(callsites.arguments) == 1

    assert entities.expressions.size() == 1
    id, _ = entities.expressions.peak()

    assert callsites.arguments[0] == id
