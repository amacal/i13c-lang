from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_slot():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.parameters.size() == 0


def can_detect_a_parameter_of_a_snippet():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mov rax, rbx; }
        """
    )

    assert entities.parameters.size() == 1
    _, value = entities.parameters.peak()

    assert value.name == b"v"


def can_detect_a_parameter_of_a_function():
    entities = prepare_entities(
        """
            fn main(x: u8) { }
        """
    )

    assert entities.parameters.size() == 1
    _, value = entities.parameters.peak()

    assert value.name == b"x"
