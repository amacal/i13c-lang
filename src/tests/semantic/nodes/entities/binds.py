from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_binds():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.binds.size() == 0


def can_detect_a_bind():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mox rax, rbx; }
        """
    )

    assert entities.binds.size() == 1
    _, value = entities.binds.peak()

    assert value.name == b"rax"
