from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_label():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.labels.size() == 0


def can_detect_a_label():
    entities = prepare_entities(
        """
            asm main() { mox rax, rbx; .me: nop; }
        """
    )

    assert entities.labels.size() == 1
    _, value = entities.labels.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert value.name == b"me"
    assert value.ctx == id
