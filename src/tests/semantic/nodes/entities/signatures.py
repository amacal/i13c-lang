from tests.semantic.nodes.entities import prepare_entities


def can_detect_a_snippet_signature():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mov rax, rbx; }
        """
    )

    assert entities.types.size() == 1
    _, value = entities.signatures.peak()

    assert value.name == b"main"
    assert len(value.slots) == 1


def can_detect_a_function_signature():
    entities = prepare_entities(
        """
            fn main(x: u8, y: u64) { }
        """
    )

    assert entities.types.size() == 2
    _, value = entities.signatures.peak()

    assert value.name == b"main"
    assert len(value.slots) == 2
