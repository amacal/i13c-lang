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
    _, value = entities.addresses.peek()

    assert value.disp is None

    assert entities.registers.size() == 1
    id, _ = entities.registers.peek()

    assert value.base == id
    assert value.indx is None


def can_detect_an_indexed_address():
    entities = prepare_entities(
        """
            asm main() { mov [rax + rbx]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peek()

    assert value.disp is None

    assert entities.registers.size() == 2
    registers = list(entities.registers.keys())

    assert entities.indices.size() == 1
    indices = list(entities.indices.keys())

    assert value.base in registers
    assert value.indx in indices


def can_detect_a_forward_address():
    entities = prepare_entities(
        """
            asm main() { jmp [rbx + 0x1234]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peek()

    assert entities.registers.size() == 1
    id, _ = entities.registers.peek()

    assert value.base == id

    assert entities.displacements.size() == 1
    id, _ = entities.displacements.peek()

    assert value.disp == id
    assert value.indx is None


def can_detect_a_backward_address():
    entities = prepare_entities(
        """
            asm main() { jmp [rbx - 0x1234]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peek()

    assert entities.registers.size() == 1
    id, _ = entities.registers.peek()

    assert value.base == id

    assert entities.displacements.size() == 1
    id, _ = entities.displacements.peek()

    assert value.disp == id
    assert value.indx is None


def can_detect_a_relative_address():
    entities = prepare_entities(
        """
            asm main() { jmp [rel @abc]; }
        """
    )

    assert entities.addresses.size() == 1
    _, value = entities.addresses.peek()

    assert entities.registers.size() == 0
    assert entities.displacements.size() == 0

    assert entities.references.size() == 1
    id, _ = entities.references.peek()

    assert value.disp == id
    assert value.indx is None
