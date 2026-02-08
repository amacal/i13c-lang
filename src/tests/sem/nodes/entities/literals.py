from i13c.semantic import model, syntax
from i13c.semantic.typing.entities.literals import Hex, Literal, LiteralId
from tests.sem import prepare_program


def can_do_nothing_without_any_literal():
    _, program = prepare_program("""
            fn main() noreturn { }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    literals = semantic.basic.literals

    assert literals.size() == 0


def can_detect_hex_literal():
    _, program = prepare_program("""
            fn main() { foo(0x476); }
        """)

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


def can_detect_two_literals_even_if_identical():
    _, program = prepare_program("""
            fn main() { foo(0x1a2b); bar(0x1a2b); }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    literals = semantic.basic.literals

    assert literals.size() == 2

    for id, value in literals.items():
        assert isinstance(id, LiteralId)
        assert isinstance(value, Literal)

        assert value.kind == b"hex"
        assert isinstance(value.target, Hex)

        assert value.target.value == 0x1A2B
        assert value.target.width == 16
