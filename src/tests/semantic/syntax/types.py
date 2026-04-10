from tests.semantic.syntax import parse_syntax_graph


def can_visit_ranges_in_a_snippet_signature() -> None:
    visitor = parse_syntax_graph(
        """
            asm main(v@rax: u8[0x01..0x02]) { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.ranges.items())) == 1


def can_visit_type_in_a_snippet_signature() -> None:
    visitor = parse_syntax_graph(
        """
            asm main(v@rax: u8) { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.types.items())) == 1


def can_visit_ranges_in_a_function_signature() -> None:
    visitor = parse_syntax_graph(
        """
            fn main(v: u8[0x01..0x02]) { foo(v); }
        """
    )

    assert len(list(visitor.graph.ranges.items())) == 1


def can_visit_type_in_a_function_signature() -> None:
    visitor = parse_syntax_graph(
        """
            fn main(v: u8) { foo(v); }
        """
    )

    assert len(list(visitor.graph.types.items())) == 1


def can_visit_ranges_in_a_value_declaration() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() {
                val v: u8[0x01..0x02] = 0x01;
            }
        """
    )

    assert len(list(visitor.graph.ranges.items())) == 1


def can_visit_type_in_a_value_declaration() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() {
                val v: u8 = 0x01;
            }
        """
    )

    assert len(list(visitor.graph.types.items())) == 1
