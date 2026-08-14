from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_allocations_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 0
    assert len(allocations.colors) == 0


def can_detect_allocations_with_a_callsite():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) noreturn { }
        fn main() noreturn { foo(0x42); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 1
    assert len(allocations.colors) == 0


def can_detect_allocations_with_of_parameters_unused():
    _, analyses = prepare_analyses("""
        fn main(abc: u32) { }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 1
    assert len(allocations.colors) == 0


def can_detect_allocations_with_of_parameters_used():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { foo(abc); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 2
    assert len(allocations.colors) == 1

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], Calling)

    assert allocations.colors[0] == 0


def can_detect_allocations_with_of_parameters_used_in_later_calls():
    _, analyses = prepare_analyses("""
        asm bar() { }
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { bar(); foo(abc); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 3
    assert len(allocations.colors) == 1

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], Calling)
    assert isinstance(allocations.values[2], Calling)

    assert allocations.colors[0] == 0


def can_detect_allocations_with_of_parameters_used_in_multiple_calls():
    _, analyses = prepare_analyses("""
        asm bar(y@rbx: u8) { }
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { bar(abc); foo(abc); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 3
    assert len(allocations.colors) == 1

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], Calling)
    assert isinstance(allocations.values[2], Calling)

    assert allocations.colors[0] == 0


def can_detect_allocations_with_of_parameters_used_in_abandoned_values():
    _, analyses = prepare_analyses("""
        asm bar(y@rbx: u8) { }
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(x: u8, y: u8) { foo(x,y); bar(y); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 4
    assert len(allocations.colors) == 2

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ParameterAcceptance)
    assert isinstance(allocations.values[2], Calling)
    assert isinstance(allocations.values[3], Calling)

    # colors are assigned backwards
    assert allocations.colors[0] == 1
    assert allocations.colors[1] == 0


def can_detect_allocations_with_of_declared_value_in_a_call():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(abc: u8) { val x: u8 = 0x13; foo(abc,x); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 3
    assert len(allocations.colors) == 2

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ValueAcceptance)
    assert isinstance(allocations.values[2], Calling)

    # colors are assigned backwards
    assert allocations.colors[0] == 1
    assert allocations.colors[1] == 0


def can_detect_allocations_with_of_declared_value_in_a_call_unused():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(abc: u8) { val x: u8 = 0x13; foo(abc,abc); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 3
    assert len(allocations.colors) == 1

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ValueAcceptance)
    assert isinstance(allocations.values[2], Calling)

    assert allocations.colors[0] == 0


def can_detect_allocations_with_of_assigned_value():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(abc: u8) { val x: u8 = abc; foo(x,x); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 3
    assert len(allocations.colors) == 2

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ValueAcceptance)
    assert isinstance(allocations.values[2], Calling)

    assert allocations.colors[0] == 1
    assert allocations.colors[1] == 0


def can_detect_allocations_with_of_three_needed_colors():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8, z@rcx: u8) { }
        fn main(abc: u8, y: u8) { val x: u8 = 0x13; foo(abc,x,y); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 4
    assert len(allocations.colors) == 3

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ParameterAcceptance)
    assert isinstance(allocations.values[2], ValueAcceptance)
    assert isinstance(allocations.values[3], Calling)

    # colors are assigned backwards
    assert allocations.colors[0] == 2
    assert allocations.colors[1] == 1
    assert allocations.colors[2] == 0


def can_detect_allocations_with_forced_spill():
    _, analyses = prepare_analyses("""
        asm foo(a@rax: u8, b@rbx: u8, c@rcx: u8) { }
        fn main(a: u8, b: u8) {
            val c: u8 = 0x13;
            val d: u8 = 0x14;
            val e: u8 = 0x15;
            val f: u8 = 0x16;
            val g: u8 = 0x17;
            val h: u8 = 0x18;
            val i: u8 = 0x19;

            foo(a,b,c);
            foo(d,e,f);
            foo(g,h,i);
        }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 12
    assert len(allocations.colors) == 8

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ParameterAcceptance)
    assert isinstance(allocations.values[2], ValueAcceptance)
    assert isinstance(allocations.values[3], ValueAcceptance)
    assert isinstance(allocations.values[4], ValueAcceptance)
    assert isinstance(allocations.values[5], ValueAcceptance)
    assert isinstance(allocations.values[6], ValueAcceptance)
    assert isinstance(allocations.values[7], ValueAcceptance)
    assert isinstance(allocations.values[8], ValueAcceptance)
    assert isinstance(allocations.values[9], Calling)
    assert isinstance(allocations.values[10], Calling)
    assert isinstance(allocations.values[11], Calling)

    # colors are assigned backwards
    assert allocations.colors[1] == 7
    assert allocations.colors[2] == 6
    assert allocations.colors[3] == 5
    assert allocations.colors[4] == 4
    assert allocations.colors[5] == 3
    assert allocations.colors[6] == 2
    assert allocations.colors[7] == 1
    assert allocations.colors[8] == 0

    # spilled values are not colored
    assert 0 not in allocations.colors
