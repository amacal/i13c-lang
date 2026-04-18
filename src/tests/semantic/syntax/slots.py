from tests.semantic.syntax import parse_syntax_graph


def can_visit_slots_in_a_snippet_signature() -> None:
    visitor = parse_syntax_graph(
        """
            asm main(v@rax: u8) { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.snippet.slots.items())) == 1


def can_visit_slots_in_a_function_signature() -> None:
    visitor = parse_syntax_graph(
        """
            fn main(x: u8, y: u64) { }
        """
    )

    assert len(list(visitor.graph.function.parameters.items())) == 2
