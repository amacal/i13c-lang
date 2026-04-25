from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.labels import LabelId
from tests.semantic.nodes.entities import prepare_entities


def can_detect_a_snippet():
    entities = prepare_entities(
        """
            asm main(v@rax: u16) { mov rax, rbx; }
        """
    )

    assert entities.snippets.size() == 1
    _, value = entities.snippets.peak()

    assert len(value.body) == 1


def can_count_a_label_in_the_snippet():
    entities = prepare_entities(
        """
            asm main() { .me: nop; }
        """
    )

    assert entities.snippets.size() == 1
    _, value = entities.snippets.peak()

    assert len(value.body) == 2
    assert isinstance(value.body[0], LabelId)
    assert isinstance(value.body[1], InstructionId)
