from i13c.core.generator import Generator
from i13c.semantic.syntax import NodesVisitor
from tests.semantic import prepare_program


def can_visit_all_nodes_in_a_snippet() -> None:
    _, program = prepare_program("""
            asm main() { mov rax, 0x1234; }
        """)

    generator = Generator()
    visitor = NodesVisitor(generator)

    program.accept(visitor)

    assert len(list(visitor.graph.snippets.items())) == 1
    assert len(list(visitor.graph.instructions.items())) == 1

    assert len(list(visitor.graph.functions.items())) == 0
    assert len(list(visitor.graph.statements.items())) == 0
    assert len(list(visitor.graph.literals.items())) == 0


def can_visit_all_nodes_in_a_function() -> None:
    _, program = prepare_program("""
            fn main() { foo(0x42); }
        """)

    generator = Generator()
    visitor = NodesVisitor(generator)

    program.accept(visitor)

    assert len(list(visitor.graph.functions.items())) == 1
    assert len(list(visitor.graph.statements.items())) == 1
    assert len(list(visitor.graph.literals.items())) == 1

    assert len(list(visitor.graph.snippets.items())) == 0
    assert len(list(visitor.graph.instructions.items())) == 0
