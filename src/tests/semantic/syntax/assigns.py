from tests.semantic.syntax import parse_syntax_graph


def can_visit_assign_statement():
    visitor = parse_syntax_graph(
        """
            fn main() { val x: u8 = 0x12; }
        """
    )

    assert len(list(visitor.graph.function.assigns.items())) == 1


def can_visit_assign_statement_with_callsite():
    visitor = parse_syntax_graph(
        """
            asm foo() -> u8@rax { }
            fn main() { val x: u8 = foo(); }
        """
    )

    assert len(list(visitor.graph.function.assigns.items())) == 1
    assert len(list(visitor.graph.function.callsites.items())) == 1
