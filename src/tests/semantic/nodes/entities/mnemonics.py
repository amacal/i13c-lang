from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_mnemonic():
    entities = prepare_entities(
        """
            asm main() noreturn { }
        """
    )

    assert entities.operands.size() == 0


def can_detect_a_mnemonic():
    entities = prepare_entities(
        """
            asm main() { call 0x1234; }
        """
    )

    assert entities.mnemonics.size() == 1
    _, value = entities.mnemonics.peak()

    assert value.name == b"call"
