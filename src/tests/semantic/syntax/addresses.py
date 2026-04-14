from tests.semantic.syntax import parse_syntax_graph


def can_visit_a_base_address() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call [rax + 0x1234]; }
        """
    )

    assert len(list(visitor.graph.addresses.items())) == 1


def can_visit_a_rip_address() -> None:
    visitor = parse_syntax_graph(
        """
            asm main() { call [rip + 0x1234]; }
        """
    )

    assert len(list(visitor.graph.addresses.items())) == 1
