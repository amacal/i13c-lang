from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_slot():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.slots.size() == 0


def can_detect_a_slot():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mox rax, rbx; }
        """
    )

    assert entities.slots.size() == 1
    _, value = entities.slots.peak()

    assert value.name == b"v"
