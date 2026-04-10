from tests.semantic.syntax import parse_syntax_graph


def can_visit_bindings_in_a_snippet_signature() -> None:
    visitor = parse_syntax_graph(
        """
            asm main(v@rax: u8) { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.bindings.items())) == 1
