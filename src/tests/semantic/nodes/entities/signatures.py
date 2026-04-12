from tests.semantic.nodes.entities import prepare_entities


def can_detect_a_snippet_signature():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mox rax, rbx; }
        """
    )

    assert entities.types.size() == 1
    _, value = entities.signatures.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert value.name == b"main"
    assert value.ctx == id
    assert len(value.slots) == 1
