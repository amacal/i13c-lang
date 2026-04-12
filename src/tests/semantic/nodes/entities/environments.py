from tests.semantic.nodes.entities import prepare_entities


def can_detect_an_environment_from_an_empty_snippet():
    entities = prepare_entities(
        """
            asm main() { }
        """
    )

    assert entities.environments.size() == 1
    _, value = entities.environments.peak()

    assert value.kind == "snippet"
    assert len(value.entries) == 0


def can_detect_an_environment_from_a_snippet_having_slots():
    entities = prepare_entities(
        """
            asm main(v@rax: u8) { mox rax, rbx; }
        """
    )

    assert entities.environments.size() == 1
    _, value = entities.environments.peak()

    assert value.kind == "snippet"
    assert len(value.entries) == 1


def can_detect_an_environment_from_a_snippet_having_labels():
    entities = prepare_entities(
        """
            asm main() { mox rax, rbx; .me: nop; }
        """
    )

    assert entities.environments.size() == 1
    _, value = entities.environments.peak()

    assert value.kind == "snippet"
    assert len(value.entries) == 1
