from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_signature_in_a_snippet_signature() -> None:
    visitor = parse_syntax_graph(
        """
            asm main(x@rax: u8, y@rbx: u64) { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.signatures.items())) == 1
