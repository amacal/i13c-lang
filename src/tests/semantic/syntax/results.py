from tests.semantic.syntax import parse_syntax_graph


def can_visit_results_in_a_snippet_signature():
    visitor = parse_syntax_graph(
        """
            asm main() -> u8@rax { }
        """
    )

    assert len(list(visitor.graph.snippet.results.items())) == 1
