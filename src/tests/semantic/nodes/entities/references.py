from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_reference():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.references.size() == 0


def can_detect_a_reference():
    entities = prepare_entities(
        """
            asm main() { mov rax, @me; }
        """
    )

    assert entities.references.size() == 1
    _, value = entities.references.peek()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peek()

    assert value.name == b"me"
    assert value.snippet.value == id.value
