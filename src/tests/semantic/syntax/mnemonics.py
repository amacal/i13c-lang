from tests.semantic.syntax import parse_syntax_graph


def can_visit_mnemonics_in_an_instruction():
    visitor = parse_syntax_graph(
        """
            asm main() { syscall; }
        """
    )

    assert len(list(visitor.graph.snippet.mnemonics.items())) == 1
