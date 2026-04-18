from tests.semantic.nodes.entities import prepare_entities


def can_detect_a_snippet():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mov rax, rbx; }
        """
    )

    assert entities.snippets.size() == 1
    _, value = entities.snippets.peak()

    assert len(value.instructions) == 1
