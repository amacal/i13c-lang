from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.resolutions.assigns import ValueAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_dflow_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 0
    assert len(dflows.forward) == 0
    assert len(dflows.backward) == 0

    assert len(dflows.control.nodes) == 2
    assert len(dflows.defs) == 2
    assert len(dflows.uses) == 2

    assert dflows.defs[dflows.entry] == []
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []


def can_detect_dflow_with_unused_parameter():
    _, analyses = prepare_analyses("""
        fn main(x: u8) { }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.values[0], ParameterAcceptance)
    assert dflows.values[0].name == b"x"
    assert dflows.values[0].type.name == b"u8"

    assert len(dflows.control.nodes) == 2
    assert len(dflows.defs) == 2
    assert len(dflows.uses) == 2

    assert dflows.defs[dflows.entry] == [0]
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []


def can_detect_dflow_with_a_callsite_using_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn main() noreturn { foo(0x42); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.values[0], Calling)
    assert dflows.values[0].signature.name == b"foo"

    assert dflows.forward[0] == []
    assert dflows.backward[0] == []

    assert len(dflows.control.nodes) == 3
    assert len(dflows.defs) == 3
    assert len(dflows.uses) == 3

    assert dflows.defs[dflows.entry] == []
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == []
    assert dflows.uses[1] == []


def can_detect_dflow_with_a_callsite_using_parameter():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar(x: u8) noreturn { foo(x); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.values):
        if isinstance(node, ParameterAcceptance):
            assert idx == 0
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert isinstance(dflows.values[dflows.forward[idx][0]], Calling)

            assert len(dflows.backward[idx]) == 0
            assert len(dflows.backward[dflows.forward[idx][0]]) == 1
            assert dflows.backward[dflows.forward[idx][0]][0] == idx

        elif isinstance(node, Calling):
            assert idx == 1
            assert node.signature.name == b"foo"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1

            assert isinstance(
                dflows.values[dflows.backward[idx][0]], ParameterAcceptance
            )

        else:
            assert False

    assert len(dflows.control.nodes) == 3
    assert len(dflows.defs) == 3
    assert len(dflows.uses) == 3

    assert dflows.defs[dflows.entry] == [0]
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == []
    assert dflows.uses[1] == [0]


def can_detect_dflow_with_a_callsite_using_value():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar() { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.values):
        if isinstance(node, ValueAcceptance):
            assert idx == 0
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert isinstance(dflows.values[dflows.forward[idx][0]], Calling)

            assert len(dflows.backward[idx]) == 0
            assert len(dflows.backward[dflows.forward[idx][0]]) == 1
            assert dflows.backward[dflows.forward[idx][0]][0] == idx

        elif isinstance(node, Calling):
            assert idx == 1
            assert node.signature.name == b"foo"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1

            assert isinstance(dflows.values[dflows.backward[idx][0]], ValueAcceptance)

        else:
            assert False

    assert len(dflows.control.nodes) == 4
    assert len(dflows.defs) == 4
    assert len(dflows.uses) == 4

    assert dflows.defs[dflows.entry] == []
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == [0]
    assert dflows.uses[1] == []

    assert dflows.defs[2] == []
    assert dflows.uses[2] == [0]


def can_detect_dflow_with_an_assignment_using_literal():
    _, analyses = prepare_analyses("""
        fn main() { val x: u8 = 0x42; }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 1
    assert len(dflows.forward) == 1
    assert len(dflows.backward) == 1

    assert isinstance(dflows.values[0], ValueAcceptance)
    assert dflows.values[0].name == b"x"
    assert dflows.values[0].type.name == b"u8"

    assert dflows.forward[0] == []
    assert dflows.backward[0] == []

    assert len(dflows.control.nodes) == 3
    assert len(dflows.defs) == 3
    assert len(dflows.uses) == 3

    assert dflows.defs[dflows.entry] == []
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == [0]
    assert dflows.uses[1] == []


def can_detect_dflow_with_an_assignment_using_parameter():
    _, analyses = prepare_analyses("""
        fn bar(x: u8) { val y: u8 = x; }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.values):
        if isinstance(node, ParameterAcceptance):
            assert idx == 0
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 0
            assert isinstance(dflows.values[dflows.forward[idx][0]], ValueAcceptance)

        elif isinstance(node, ValueAcceptance):
            assert idx == 1
            assert node.name == b"y"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1
            assert isinstance(
                dflows.values[dflows.backward[idx][0]], ParameterAcceptance
            )

        else:
            assert False

    assert len(dflows.control.nodes) == 3
    assert len(dflows.defs) == 3
    assert len(dflows.uses) == 3

    assert dflows.defs[dflows.entry] == [0]
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == [1]
    assert dflows.uses[1] == [0]


def can_detect_dflow_with_a_chain_of_parameter_to_value_to_callsite():
    _, analyses = prepare_analyses("""
        asm foo(x@rbx: u8) { }
        fn bar(x: u8) { val y: u8 = x; foo(y); }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 3
    assert len(dflows.forward) == 3
    assert len(dflows.backward) == 3

    for idx, node in enumerate(dflows.values):
        if isinstance(node, ParameterAcceptance):
            assert idx == 0
            assert node.name == b"x"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 0
            assert isinstance(dflows.values[dflows.forward[idx][0]], ValueAcceptance)

        elif isinstance(node, ValueAcceptance):
            assert idx == 1
            assert node.name == b"y"
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 1
            assert isinstance(
                dflows.values[dflows.backward[idx][0]], ParameterAcceptance
            )
            assert isinstance(dflows.values[dflows.forward[idx][0]], Calling)

        else:
            assert node.signature.name == b"foo"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1
            assert isinstance(dflows.values[dflows.backward[idx][0]], ValueAcceptance)

    assert len(dflows.control.nodes) == 4
    assert len(dflows.defs) == 4
    assert len(dflows.uses) == 4

    assert dflows.defs[dflows.entry] == [0]
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == [1]
    assert dflows.uses[1] == [0]

    assert dflows.defs[2] == []
    assert dflows.uses[2] == [1]


def can_detect_dflow_with_an_assignment_using_value():
    _, analyses = prepare_analyses("""
        fn bar() { val x: u8 = 0x42; val y: u8 = x; }
    """)

    assert analyses.dflows is not None
    assert analyses.dflows.size() == 1
    _, dflows = analyses.dflows.peak()

    assert len(dflows.values) == 2
    assert len(dflows.forward) == 2
    assert len(dflows.backward) == 2

    for idx, node in enumerate(dflows.values):
        assert isinstance(node, ValueAcceptance)

        if node.name == b"x":
            assert idx == 0
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 1
            assert len(dflows.backward[idx]) == 0

            assert dflows.forward[idx][0] != idx
            assert isinstance(dflows.values[dflows.forward[idx][0]], ValueAcceptance)

        elif node.name == b"y":
            assert idx == 1
            assert node.type.name == b"u8"

            assert len(dflows.forward[idx]) == 0
            assert len(dflows.backward[idx]) == 1

            assert dflows.backward[idx][0] != idx
            assert isinstance(dflows.values[dflows.backward[idx][0]], ValueAcceptance)

        else:
            assert False

    assert len(dflows.control.nodes) == 4
    assert len(dflows.defs) == 4
    assert len(dflows.uses) == 4

    assert dflows.defs[dflows.entry] == []
    assert dflows.defs[dflows.exit] == []

    assert dflows.uses[dflows.entry] == []
    assert dflows.uses[dflows.exit] == []

    assert dflows.defs[1] == [0]
    assert dflows.uses[1] == []

    assert dflows.defs[2] == [1]
    assert dflows.uses[2] == [0]
