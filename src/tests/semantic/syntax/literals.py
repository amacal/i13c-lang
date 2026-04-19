from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_literal() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() { val x: u16 = 0x1234; }
        """
    )

    assert len(list(visitor.graph.function.literals.items())) == 1
