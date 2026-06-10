from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.resolutions.assigns import ValueAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_dflow_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() noreturn { }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 0
    assert len(dflows.forward) == 0
    assert len(dflows.backward) == 0


def can_detect_dflow_with_unused_parameter():
    _, analyses = prepare_analyses("""
        fn bar(x: u8) noreturn { }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.nodes[0], ParameterAcceptance)
    assert dflows.nodes[0].name == b"x"
    assert dflows.nodes[0].type.name == b"u8"



def can_detect_dflow_with_a_callsite_using_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn main() noreturn { foo(0x42); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.nodes[0], Calling)
    assert dflows.nodes[0].signature.name == b"foo"

    assert dflows.forward[0] == []
    assert dflows.backward[0] == []


def can_detect_dflow_with_a_callsite_using_parameter():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar(x: u8) noreturn { foo(x); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.nodes):
        if isinstance(node, ParameterAcceptance):
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert isinstance(dflows.nodes[dflows.forward[idx][0]], Calling)

            assert len(dflows.backward[idx]) == 0
            assert len(dflows.backward[dflows.forward[idx][0]]) == 1
            assert dflows.backward[dflows.forward[idx][0]][0] == idx

        elif isinstance(node, Calling):
            assert node.signature.name == b"foo"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1

            assert isinstance(
                dflows.nodes[dflows.backward[idx][0]], ParameterAcceptance
            )

        else:
            assert False


def can_detect_dflow_with_a_callsite_using_callsite_with_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar() noreturn { foo(0x42); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.nodes[0], Calling)
    assert dflows.nodes[0].signature.name == b"foo"

    assert len(dflows.forward[0]) == 0
    assert len(dflows.backward[0]) == 0


def can_detect_dflow_with_a_callsite_using_callsite_with_value():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar() noreturn { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.nodes):
        if isinstance(node, ValueAcceptance):
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert isinstance(dflows.nodes[dflows.forward[idx][0]], Calling)

            assert len(dflows.backward[idx]) == 0
            assert len(dflows.backward[dflows.forward[idx][0]]) == 1
            assert dflows.backward[dflows.forward[idx][0]][0] == idx

        elif isinstance(node, Calling):
            assert node.signature.name == b"foo"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1

            assert isinstance(dflows.nodes[dflows.backward[idx][0]], ValueAcceptance)

        else:
            assert False


def can_detect_dflow_with_an_assignment_using_literal():
    _, analyses = prepare_analyses("""
        fn main() noreturn { val x: u8 = 0x42; }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.nodes[0], ValueAcceptance)
    assert dflows.nodes[0].name == b"x"
    assert dflows.nodes[0].type.name == b"u8"

    assert dflows.forward[0] == []
    assert dflows.backward[0] == []


def can_detect_dflow_with_an_assignment_using_parameter():
    _, analyses = prepare_analyses("""
        fn bar(x: u8) noreturn { val y: u8 = x; }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.nodes):
        if isinstance(node, ParameterAcceptance):
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 0
            assert isinstance(dflows.nodes[dflows.forward[idx][0]], ValueAcceptance)

        elif isinstance(node, ValueAcceptance):
            assert node.name == b"y"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1
            assert isinstance(
                dflows.nodes[dflows.backward[idx][0]], ParameterAcceptance
            )

        else:
            assert False


def can_detect_dflow_with_a_chain_of_parameter_to_value_to_callsite():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar(x: u8) noreturn { val y: u8 = x; foo(y); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 3
    assert len(dflows.forward) == 3
    assert len(dflows.backward) == 3

    for idx, node in enumerate(dflows.nodes):
        if isinstance(node, ParameterAcceptance):
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 0
            assert isinstance(dflows.nodes[dflows.forward[idx][0]], ValueAcceptance)

        elif isinstance(node, ValueAcceptance):
            assert node.name == b"y"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 1
            assert isinstance(dflows.nodes[dflows.backward[idx][0]], ParameterAcceptance)
            assert isinstance(dflows.nodes[dflows.forward[idx][0]], Calling)

        elif isinstance(node, Calling):
            assert node.signature.name == b"foo"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1
            assert isinstance(dflows.nodes[dflows.backward[idx][0]], ValueAcceptance)

        else:
            assert False


def can_detect_dflow_with_an_assignment_using_value():
    _, analyses = prepare_analyses("""
        fn bar() noreturn { val x: u8 = 0x42; val y: u8 = x; }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.nodes) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.nodes):
        assert isinstance(node, ValueAcceptance)

        if node.name == b"x":
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 0

            assert dflows.forward[idx][0] != idx
            assert isinstance(dflows.nodes[dflows.forward[idx][0]], ValueAcceptance)

        elif node.name == b"y":
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1

            assert dflows.backward[idx][0] != idx
            assert isinstance(dflows.nodes[dflows.backward[idx][0]], ValueAcceptance)

        else:
            assert False
