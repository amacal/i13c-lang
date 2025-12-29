from i13c.sem import literal, model, syntax
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
    literals = semantic.literals

    assert len(literals) == 1
    id, value = literals.popitem()

    assert isinstance(id, literal.LiteralId)
    assert isinstance(value, literal.Literal)

    assert value.kind == b"hex"
    assert isinstance(value.target, literal.Hex)

    assert value.target.value == 0x476
    assert value.target.width == 16
