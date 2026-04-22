from tests.semantic.syntax import parse_syntax_graph


def can_visit_assign_statement() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() { val x: u8 = 0x12; }
        """
    )

    assert len(list(visitor.graph.function.assigns.items())) == 1
