from tests.semantic.syntax import parse_syntax_graph


def can_visit_registers_in_an_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { mov rax, 0x1234; }
        """
    )

    assert len(list(visitor.graph.registers.items())) == 1


def can_visit_registers_in_an_base_of_an_address() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call [rbx + 0x1234]; }
        """
    )

    assert len(list(visitor.graph.registers.items())) == 1
