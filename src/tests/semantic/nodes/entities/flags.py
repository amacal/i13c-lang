from tests.semantic.nodes.entities import prepare_entities


def can_detect_a_snippet_flags_noreturn():
    entities = prepare_entities(
        """
            asm main() noreturn { mov rax, rbx; }
        """
    )

    assert entities.flags.size() == 1
    _, value = entities.flags.peak()

    assert value.noreturn is True
    assert value.clobbers is None


def can_detect_a_snippet_flags_clobbers():
    entities = prepare_entities(
        """
            asm main() clobbers rax, rbx { mov rax, rbx; }
        """
    )

    assert entities.flags.size() == 1
    _, value = entities.flags.peak()

    assert value.noreturn is None
    assert len(value.clobbers or []) == 2


def can_detect_a_function_noreturn():
    entities = prepare_entities(
        """
            fn main() noreturn { }
        """
    )

    assert entities.flags.size() == 1
    _, value = entities.flags.peak()

    assert value.noreturn is True
    assert value.clobbers is None
