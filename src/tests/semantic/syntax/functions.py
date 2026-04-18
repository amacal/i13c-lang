from tests.semantic.syntax import parse_syntax_graph


def can_visit_all_nodes_in_a_function() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() { foo(0x42); }
        """
    )

    assert len(list(visitor.graph.function.functions.items())) == 1
    assert len(list(visitor.graph.function.statements.items())) == 1
    assert len(list(visitor.graph.function.literals.items())) == 1
