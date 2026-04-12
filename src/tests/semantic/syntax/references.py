from tests.semantic.syntax import parse_syntax_graph


def can_visit_references_in_an_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { mov rax, @x; }
        """
    )

    assert len(list(visitor.graph.references.items())) == 1
