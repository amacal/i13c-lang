from tests.semantic.syntax import parse_syntax_graph


def can_visit_all_nodes_in_a_snippet() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.snippets.items())) == 1
    assert len(list(visitor.graph.instructions.items())) == 1

    assert len(list(visitor.graph.functions.items())) == 0
    assert len(list(visitor.graph.statements.items())) == 0
    assert len(list(visitor.graph.literals.items())) == 0
