from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_operand():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.operands.size() == 0


def can_detect_an_immediate_operand():
    entities = prepare_entities(
        """
            asm main() { call 0x1234; }
        """
    )

    assert entities.operands.size() == 1
    _, value = entities.operands.peek()

    assert entities.immediates.size() == 1
    id, _ = entities.immediates.peek()

    assert value.kind == "immediate"
    assert value.target == id


def can_detect_a_register_operand():
    entities = prepare_entities(
        """
            asm main() { call rax; }
        """
    )

    assert entities.operands.size() == 1
    _, value = entities.operands.peek()

    assert entities.registers.size() == 1
    id, _ = entities.registers.peek()

    assert value.kind == "register"
    assert value.target == id


def can_detect_a_reference_operand():
    entities = prepare_entities(
        """
            asm main() { call @me; }
        """
    )

    assert entities.operands.size() == 1
    _, value = entities.operands.peek()

    assert entities.references.size() == 1
    id, _ = entities.references.peek()

    assert value.kind == "reference"
    assert value.target == id
