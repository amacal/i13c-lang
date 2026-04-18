from tests.semantic.syntax import parse_syntax_graph


def can_visit_an_instruction_without_any_opperand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { nop; }
        """
    )

    assert len(list(visitor.graph.snippet.instructions.items())) == 1


def can_visit_an_instruction_with_some_operands() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.snippet.instructions.items())) == 1
