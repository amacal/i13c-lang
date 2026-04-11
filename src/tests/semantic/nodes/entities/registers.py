from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_immediate():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.registers.size() == 0


def can_detect_a_register_as_the_operand():
    entities = prepare_entities(
        """
            asm main() { mox rax, 0x1234; }
        """
    )

    assert entities.registers.size() == 1
    _, value = entities.registers.peak()

    assert value.name == b"rax"
