from i13c.sem import model, syntax
from i13c.sem.typing.entities.callsites import CallSite, CallSiteId
from i13c.sem.typing.entities.literals import Hex, LiteralId
from tests.sem import prepare_program


def can_do_nothing_without_any_callsite():
    _, program = prepare_program(
        """
            fn main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callsites = semantic.basic.callsites

    assert callsites.size() == 0


def can_build_callsite_with_no_arguments():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callsites = semantic.basic.callsites

    assert callsites.size() == 1
    id, value = callsites.pop()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSite)

    assert value.callee.name == b"foo"
    assert len(value.arguments) == 0


def can_build_callsite_with_single_argument():
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

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSite)

    assert value.callee.name == b"foo"
    assert len(value.arguments) == 1

    argument = value.arguments[0]
    assert argument.kind == b"literal"

    assert isinstance(argument.target, LiteralId)
    value = semantic.basic.literals.get(argument.target)

    assert value.kind == b"hex"
    assert isinstance(value.target, Hex)
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
    values = [0x01, 0x02, 0x03]

    for argument, expected in zip(value.arguments, values):
        assert argument.kind == b"literal"
        assert isinstance(argument.target, LiteralId)

        value = semantic.basic.literals.get(argument.target)

        assert value.kind == b"hex"
        assert isinstance(value.target, Hex)

        assert value.target.value == expected
        assert value.target.width == 8
