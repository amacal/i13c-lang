from i13c.sem import callsite, literal, model, syntax
from tests.sem import prepare_program


def can_build_semantic_model_callsites():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callsites = semantic.basic.callsites

    assert callsites.size() == 1
    id, value = callsites.pop()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, callsite.CallSite)

    assert value.callee.name == b"foo"
    assert len(value.arguments) == 1

    argument = value.arguments[0]
    assert argument.kind == b"literal"

    assert isinstance(argument.target, literal.LiteralId)
    value = semantic.basic.literals.get(argument.target)

    assert value.kind == b"hex"
    assert isinstance(value.target, literal.Hex)

    assert value.target.value == 0x42
    assert value.target.width == 8


def can_build_callsite_with_multiple_arguments():
    _, program = prepare_program(
        """
            fn main() { foo(0x1, 0x2, 0x3); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callsites = semantic.basic.callsites

    assert callsites.size() == 1
    _, value = callsites.pop()

    assert len(value.arguments) == 3
    values = [0x1, 0x2, 0x3]

    for argument, expected in zip(value.arguments, values):
        assert argument.kind == b"literal"
        assert isinstance(argument.target, callsite.LiteralId)

        value = semantic.basic.literals.get(argument.target)

        assert value.kind == b"hex"
        assert isinstance(value.target, literal.Hex)

        assert value.target.value == expected
        assert value.target.width == 8
