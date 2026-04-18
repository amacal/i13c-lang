from tests.semantic.syntax import parse_syntax_graph


def can_visit_mnemonics_in_an_instruction() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { syscall; }
        """
    )

    assert len(list(visitor.graph.mnemonics.items())) == 1
