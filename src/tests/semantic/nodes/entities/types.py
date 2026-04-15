from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_type():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.ranges.size() == 0


def can_detect_a_type():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mov rax, rbx; }
        """
    )

    assert entities.types.size() == 1
    _, value = entities.types.peak()

    assert value.name == b"u16"
    assert value.range is None


def can_detect_a_type_with_a_range():
    entities = prepare_entities(
        """
            asm main(v@rax: u8[0x01..0x02]) { mov rax, rbx; }
        """
    )

    assert entities.types.size() == 1
    _, value = entities.types.peak()

    assert value.name == b"u8"
    assert value.range is not None
