from tests.semantic.syntax import parse_syntax_graph


def can_visit_references_in_operand() -> None:
    visitor = parse_syntax_graph("""
        asm main() { jmp @start; }
    """)

    assert len(list(visitor.graph.snippet.references.items())) == 1


def can_visit_reference_in_relocated_address() -> None:
    visitor = parse_syntax_graph("""
        asm main() { jmp [rel @start]; }
    """)

    assert len(list(visitor.graph.snippet.references.items())) == 1
