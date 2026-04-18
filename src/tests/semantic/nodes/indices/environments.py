from tests.semantic.nodes.indices import prepare_indices


def can_index_a_snippet_environment_without_entries():
    _, indices = prepare_indices(
        """
            asm main() { }
        """
    )

    assert indices.environments_by_snippets is not None
    assert indices.environments_by_snippets.size() == 1

    _, acceptance = indices.environments_by_snippets.peak()

    assert len(acceptance.entries) == 0
