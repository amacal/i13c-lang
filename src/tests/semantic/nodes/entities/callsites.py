from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.literals import Hex, LiteralId
from tests.semantic import prepare_program


def can_do_nothing_without_any_callsite():
    _, program = prepare_program("""
        fn main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callsites = semantic.entities.callsites

    assert callsites.size() == 0


def can_build_callsite_with_no_arguments():
    _, program = prepare_program("""
        fn main() noreturn { foo(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callsites = semantic.entities.callsites

    assert callsites.size() == 1
    id, value = callsites.pop()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSite)

    assert value.callee.data == b"foo"
    assert len(value.arguments) == 0


def can_build_callsite_with_single_argument():
    _, program = prepare_program("""
        fn main() noreturn { foo(0x42); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callsites = semantic.entities.callsites

    assert callsites.size() == 1
    id, value = callsites.pop()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSite)

    assert value.callee.data == b"foo"
    assert len(value.arguments) == 1

    argument = value.arguments[0]
    assert argument.kind == b"literal"

    assert isinstance(argument.target, LiteralId)
    value = semantic.entities.literals.get(argument.target)

    assert value.kind == b"hex"
    assert isinstance(value.target, Hex)
    assert value.target.data == bytes([0x42])
    assert value.target.width == 8


def can_build_callsite_with_multiple_arguments():
    _, program = prepare_program("""
        fn main() { foo(0x01, 0x02, 0x03); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callsites = semantic.entities.callsites

    assert callsites.size() == 1
    _, value = callsites.pop()

    assert len(value.arguments) == 3
    values = [0x01, 0x02, 0x03]

    for argument, expected in zip(value.arguments, values):
        assert argument.kind == b"literal"
        assert isinstance(argument.target, LiteralId)

        value = semantic.entities.literals.get(argument.target)

        assert value.kind == b"hex"
        assert isinstance(value.target, Hex)

        assert value.target.data.hex(" ") == f"{expected:02x}"
        assert value.target.width == 8
