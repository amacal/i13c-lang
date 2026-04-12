from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_label() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { mov rax, @x; .label: nop; }
        """
    )

    assert len(list(visitor.graph.labels.items())) == 1
