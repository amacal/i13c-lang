from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_register_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call rax; }
        """
    )

    assert len(list(visitor.graph.operands.items())) == 1


def can_visit_an_immediate_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call 0x1234; }
        """
    )

    assert len(list(visitor.graph.operands.items())) == 1


def can_visit_a_reference_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main(x@rax: u16) { call @x; }
        """
    )

    assert len(list(visitor.graph.operands.items())) == 1


def can_visit_a_base_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call [rax + 0x1234]; }
        """
    )

    assert len(list(visitor.graph.operands.items())) == 1


def can_visit_a_rip_operand() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call [rip + 0x1234]; }
        """
    )

    assert len(list(visitor.graph.operands.items())) == 1
