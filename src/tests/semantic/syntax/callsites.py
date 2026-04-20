from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_callsite_node_in_a_function() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() { foo(0x42); }
        """
    )

    assert len(list(visitor.graph.function.callsites.items())) == 1
