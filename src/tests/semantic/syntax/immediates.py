from tests.semantic.syntax import parse_syntax_graph


def can_visit_immediates_in_an_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.immediates.items())) == 1
