from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_immediate():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.immediates.size() == 0


def can_detect_an_immediate_as_the_operand():
    entities = prepare_entities(
        """
            asm main() { mox rax, 0x1234; }
        """
    )

    assert entities.immediates.size() == 1
    _, value = entities.immediates.peak()

    assert value.value.width == 16
    assert value.value.data.hex() == "1234"
