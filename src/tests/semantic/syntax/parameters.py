from tests.semantic.syntax import parse_syntax_graph


def can_visit_parameters_in_a_function_signature() -> None:
    visitor = parse_syntax_graph(
        """
            fn main(v: u8) { call(); }
        """
    )

    assert len(list(visitor.graph.function.parameters.items())) == 1


def can_visit_parameters_in_a_function_signature_with_multiple_parameters() -> None:
    visitor = parse_syntax_graph(
        """
            fn main(x: u8, y: u64) { }
        """
    )

    assert len(list(visitor.graph.function.parameters.items())) == 2
