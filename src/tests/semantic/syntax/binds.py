from tests.semantic.syntax import parse_syntax_graph


def can_visit_binds_in_a_snippet_signature_slot():
    visitor = parse_syntax_graph("""
        asm main(v@rax: u8) { mov rax, 0x1234; }
    """)

    assert len(list(visitor.graph.snippet.binds.items())) == 1


def can_visit_binds_in_a_snippet_signature_result():
    visitor = parse_syntax_graph("""
        asm main() -> u8@rax { mov rax, 0x1234; }
    """)

    assert len(list(visitor.graph.snippet.binds.items())) == 1
