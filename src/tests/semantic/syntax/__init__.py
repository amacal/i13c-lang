from i13c.core.generator import Generator
from i13c.semantic.syntax import NodesVisitor
from i13c.syntax.tree.core import Path
from tests.semantic import prepare_program


def parse_syntax_graph(code: str) -> NodesVisitor:
    _, program = prepare_program(code)

    generator = Generator()
    visitor = NodesVisitor(generator)

    program.accept(visitor, Path())
    return visitor


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


def can_visit_all_nodes_in_a_function() -> None:
    visitor = parse_syntax_graph(
        """
            fn main() { foo(0x42); }
        """
    )

    assert len(list(visitor.graph.functions.items())) == 1
    assert len(list(visitor.graph.statements.items())) == 1
    assert len(list(visitor.graph.literals.items())) == 1

    assert len(list(visitor.graph.snippets.items())) == 0
    assert len(list(visitor.graph.instructions.items())) == 0
