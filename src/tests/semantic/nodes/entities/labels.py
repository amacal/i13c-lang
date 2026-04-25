from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.labels import EndOfSnippet
from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_label():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.labels.size() == 0


def can_detect_a_label():
    entities = prepare_entities(
        """
            asm main() { mov rax, rbx; .me: nop; }
        """
    )

    assert entities.labels.size() == 1
    _, value = entities.labels.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert value.name == b"me"
    assert value.snippet.value == id.value

    assert isinstance(value.target, InstructionId)


def can_detect_a_label_at_the_end():
    entities = prepare_entities(
        """
            asm main() { mov rax, rbx; .me: }
        """
    )

    assert entities.labels.size() == 1
    _, value = entities.labels.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert value.name == b"me"
    assert value.snippet.value == id.value

    assert isinstance(value.target, EndOfSnippet)


def can_detect_a_two_same_labels():
    entities = prepare_entities(
        """
            asm main() { .me1: .me2: nop; }
        """
    )

    assert entities.labels.size() == 2

    assert entities.instructions.size() == 1
    id, _ = entities.instructions.peak()

    for value in entities.labels.values():
        assert value.name in (b"me1", b"me2")

        assert isinstance(value.target, InstructionId)
        assert value.target == id
