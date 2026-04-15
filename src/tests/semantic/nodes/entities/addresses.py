from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_address():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.addresses.size() == 0


def can_detect_an_offsetless_address():
    entities = prepare_entities(
        """
            asm main() { mov [rax]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peak()

    assert value.offset is None

    assert entities.registers.size() == 1
    id, _ = entities.registers.peak()

    assert value.base == id


def can_detect_a_forward_address():
    entities = prepare_entities(
        """
            asm main() { call [rbx + 0x1234]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peak()

    assert value.offset is not None
    assert value.offset.kind == "forward"

    assert entities.registers.size() == 1
    id, _ = entities.registers.peak()

    assert value.base == id

    assert entities.immediates.size() == 1
    id, _ = entities.immediates.peak()

    assert value.offset.value == id


def can_detect_a_backward_address():
    entities = prepare_entities(
        """
            asm main() { call [rbx - 0x1234]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peak()

    assert value.offset is not None
    assert value.offset.kind == "backward"

    assert entities.registers.size() == 1
    id, _ = entities.registers.peak()

    assert value.base == id

    assert entities.immediates.size() == 1
    id, _ = entities.immediates.peak()

    assert value.offset.value == id
