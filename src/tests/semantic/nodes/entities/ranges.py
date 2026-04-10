from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_range():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.ranges.size() == 0


def can_detect_a_range():
    entities = prepare_entities(
        """
            asm main(v@rax: u8[0x01..0x02]) { mox rax, rbx; }
        """
    )

    assert entities.ranges.size() == 1
    _, value = entities.ranges.peak()

    assert value.lower.width == 8
    assert value.lower.data.hex() == "01"

    assert value.upper.width == 8
    assert value.upper.data.hex() == "02"
