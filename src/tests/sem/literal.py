from i13c.sem import model, syntax
from i13c.sem.typing.entities.literals import Hex, Literal, LiteralId
from tests.sem import prepare_program


def can_build_semantic_model_literals():
    _, program = prepare_program(
        """
            fn main() { foo(0x476); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    literals = semantic.basic.literals

    assert literals.size() == 1
    id, value = literals.pop()

    assert isinstance(id, LiteralId)
    assert isinstance(value, Literal)

    assert value.kind == b"hex"
    assert isinstance(value.target, Hex)

    assert value.target.value == 0x476
    assert value.target.width == 16
