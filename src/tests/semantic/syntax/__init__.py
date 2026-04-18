from i13c.core.generator import Generator
from i13c.semantic.syntax import NodesVisitor
from i13c.syntax.tree.core import Path
from tests.semantic import prepare_program


def parse_syntax_graph(code: str) -> NodesVisitor:
    _, program = prepare_program(code)

    path = Path()
    generator = Generator()
    visitor = NodesVisitor(generator)

    program.accept(visitor, path)
    assert path.is_empty()

    return visitor
