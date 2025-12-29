from i13c.sem.syntax import NodesVisitor
from tests.sem import prepare_program


def can_visit_all_nodes_in_a_snippet() -> None:
    _, program = prepare_program(
        """
            asm main() { mov rax, 0x1234; }
        """
    )

    visitor = NodesVisitor()
    program.accept(visitor)

    assert len(list(visitor.nodes.snippets.items())) == 1
    assert len(list(visitor.nodes.instructions.items())) == 1

    assert len(list(visitor.nodes.functions.items())) == 0
    assert len(list(visitor.nodes.statements.items())) == 0
    assert len(list(visitor.nodes.literals.items())) == 0


def can_visit_all_nodes_in_a_function() -> None:
    _, program = prepare_program(
        """
            fn main() { foo(0x42); }
        """
    )

    visitor = NodesVisitor()
    program.accept(visitor)

    assert len(list(visitor.nodes.functions.items())) == 1
    assert len(list(visitor.nodes.statements.items())) == 1
    assert len(list(visitor.nodes.literals.items())) == 1

    assert len(list(visitor.nodes.snippets.items())) == 0
    assert len(list(visitor.nodes.instructions.items())) == 0
