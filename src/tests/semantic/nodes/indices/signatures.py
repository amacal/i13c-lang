from tests.semantic.nodes.indices import prepare_indices


def can_index_signature_by_snippet_name():
    _, indices = prepare_indices(
        """
            asm main() { }
        """
    )

    assert indices.signatures_by_names is not None
    assert indices.signatures_by_names.size() == 1

    _, acceptance = indices.signatures_by_names.peak()

    assert len(acceptance) == 1
    assert acceptance[0].name == b"main"


def can_index_multiple_signatures_by_snippet_name():
    _, indices = prepare_indices(
        """
            asm main() { }
            asm main() { }
        """
    )

    assert indices.signatures_by_names is not None
    assert indices.signatures_by_names.size() == 1

    _, acceptance = indices.signatures_by_names.peak()

    assert len(acceptance) == 2
    assert acceptance[0].id != acceptance[1].id

    assert acceptance[0].name == b"main"
    assert acceptance[1].name == b"main"
