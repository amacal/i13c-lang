from i13c.semantic.typing.analyses.callings import Calling, CallingClobber
from i13c.semantic.typing.analyses.cflows import FlowNode
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_liveness_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.values) == 0
    assert len(liveness.nodes) == 2

    assert len(liveness.live_in) == 2
    assert len(liveness.live_out) == 2

    for idx in range(len(liveness.nodes)):
        assert len(liveness.live_in[idx]) == 0
        assert len(liveness.live_out[idx]) == 0


def can_detect_liveness_with_a_callsite():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) noreturn { }
        fn main() noreturn { foo(0x42); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 3
    assert len(liveness.values) == 1

    assert len(liveness.live_in) == 3
    assert len(liveness.live_out) == 3

    for idx in range(len(liveness.nodes)):
        assert len(liveness.live_in[idx]) == 0
        assert len(liveness.live_out[idx]) == 0


def can_detect_liveness_with_a_callsite_with_clobbers():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) clobbers rcx { }
        fn main() { foo(0x42); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 3
    assert len(liveness.values) == 2

    assert len(liveness.live_in) == 3
    assert len(liveness.live_out) == 3

    assert len(liveness.live_in[0]) == 0
    assert len(liveness.live_out[0]) == 0

    assert len(liveness.live_in[1]) == 0
    assert len(liveness.live_out[1]) == 0

    assert len(liveness.clobbers[1]) == 1
    assert liveness.clobbers[1] == {1}

    assert isinstance(liveness.values[1], CallingClobber)

    assert len(liveness.live_in[2]) == 0
    assert len(liveness.live_out[2]) == 0


def can_detect_liveness_with_of_parameters_unused():
    _, analyses = prepare_analyses("""
        fn main(abc: u32) { }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 2
    assert len(liveness.values) == 1

    assert len(liveness.live_in) == 2
    assert len(liveness.live_out) == 2

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == set()

    assert liveness.live_in[1] == set()
    assert liveness.live_out[1] == set()


def can_detect_liveness_with_of_parameters_used():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { foo(abc); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 3
    assert len(liveness.values) == 2

    assert len(liveness.live_in) == 3
    assert len(liveness.live_out) == 3

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0}

    assert liveness.live_in[1] == {0}
    assert liveness.live_out[1] == set()

    assert liveness.live_in[2] == set()
    assert liveness.live_out[2] == set()


def can_detect_liveness_with_of_parameters_used_in_later_calls():
    _, analyses = prepare_analyses("""
        asm bar() { }
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { bar(); foo(abc); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 4
    assert len(liveness.values) == 3

    assert len(liveness.live_in) == 4
    assert len(liveness.live_out) == 4

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.nodes[2], FlowNode)

    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], Calling)
    assert isinstance(liveness.values[2], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0}

    assert liveness.live_in[1] == {0}
    assert liveness.live_out[1] == {0}

    assert liveness.live_in[2] == {0}
    assert liveness.live_out[2] == set()

    assert liveness.live_in[3] == set()
    assert liveness.live_out[3] == set()


def can_detect_liveness_with_of_parameters_used_in_multiple_calls():
    _, analyses = prepare_analyses("""
        asm bar(y@rbx: u8) { }
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { bar(abc); foo(abc); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 4
    assert len(liveness.values) == 3

    assert len(liveness.live_in) == 4
    assert len(liveness.live_out) == 4

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.nodes[2], FlowNode)

    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], Calling)
    assert isinstance(liveness.values[2], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0}

    assert liveness.live_in[1] == {0}
    assert liveness.live_out[1] == {0}

    assert liveness.live_in[2] == {0}
    assert liveness.live_out[2] == set()

    assert liveness.live_in[3] == set()
    assert liveness.live_out[3] == set()


def can_detect_liveness_with_of_parameters_used_in_abandoned_values():
    _, analyses = prepare_analyses("""
        asm bar(y@rbx: u8) { }
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(x: u8, y: u8) { foo(x,y); bar(y); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 4
    assert len(liveness.values) == 4

    assert len(liveness.live_in) == 4
    assert len(liveness.live_out) == 4

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.nodes[2], FlowNode)

    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], ParameterAcceptance)
    assert isinstance(liveness.values[2], Calling)
    assert isinstance(liveness.values[3], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0, 1}

    assert liveness.live_in[1] == {0, 1}
    assert liveness.live_out[1] == {1}

    assert liveness.live_in[2] == {1}
    assert liveness.live_out[2] == set()

    assert liveness.live_in[3] == set()
    assert liveness.live_out[3] == set()


def can_detect_liveness_with_of_declared_value_in_a_call():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(abc: u8) { val x: u8 = 0x13; foo(abc,x); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 4
    assert len(liveness.values) == 4

    assert len(liveness.live_in) == 4
    assert len(liveness.live_out) == 4

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.nodes[2], FlowNode)

    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], ValueAcceptance)
    assert isinstance(liveness.values[2], LiteralAcceptance)
    assert isinstance(liveness.values[3], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0}

    assert liveness.live_in[1] == {0}
    assert liveness.live_out[1] == {0, 1}

    assert liveness.live_in[2] == {0, 1}
    assert liveness.live_out[2] == set()

    assert liveness.live_in[3] == set()
    assert liveness.live_out[3] == set()


def can_detect_liveness_with_of_declared_value_in_a_call_unused():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(abc: u8) { val x: u8 = 0x13; foo(abc,abc); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 4
    assert len(liveness.values) == 4

    assert len(liveness.live_in) == 4
    assert len(liveness.live_out) == 4

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.nodes[2], FlowNode)

    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], ValueAcceptance)
    assert isinstance(liveness.values[2], LiteralAcceptance)
    assert isinstance(liveness.values[3], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0}

    assert liveness.live_in[1] == {0}
    assert liveness.live_out[1] == {0}

    assert liveness.live_in[2] == {0}
    assert liveness.live_out[2] == set()

    assert liveness.live_in[3] == set()
    assert liveness.live_out[3] == set()


def can_detect_liveness_with_of_assigned_value():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(abc: u8) { val x: u8 = abc; foo(x,x); }
    """)

    assert analyses.liveness is not None
    assert analyses.liveness.size() == 1
    _, liveness = analyses.liveness.peak()

    assert len(liveness.nodes) == 4
    assert len(liveness.values) == 3

    assert len(liveness.live_in) == 4
    assert len(liveness.live_out) == 4

    assert isinstance(liveness.nodes[1], FlowNode)
    assert isinstance(liveness.nodes[2], FlowNode)

    assert isinstance(liveness.values[0], ParameterAcceptance)
    assert isinstance(liveness.values[1], ValueAcceptance)
    assert isinstance(liveness.values[2], Calling)

    assert liveness.live_in[0] == set()
    assert liveness.live_out[0] == {0}

    assert liveness.live_in[1] == {0}
    assert liveness.live_out[1] == {1}

    assert liveness.live_in[2] == {1}
    assert liveness.live_out[2] == set()

    assert liveness.live_in[3] == set()
    assert liveness.live_out[3] == set()
