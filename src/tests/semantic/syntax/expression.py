from tests.semantic.syntax import parse_syntax_graph


def can_visit_expression_in_value_declaration() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() { val x: u8 = abc; }
        """
    )

    assert len(list(visitor.graph.function.expressions.items())) == 1
