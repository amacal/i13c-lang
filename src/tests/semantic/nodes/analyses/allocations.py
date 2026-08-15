from i13c.semantic.typing.analyses.callings import Calling, CallingClobber
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
    assert len(allocations.spills) == 0


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
    assert len(allocations.spills) == 0


def can_detect_allocations_with_a_clobber():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) clobbers rcx { }
        fn main() { foo(0x42); }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 2
    assert len(allocations.colors) == 0
    assert len(allocations.spills) == 0


def can_detect_allocations_with_of_parameters_unused():
    _, analyses = prepare_analyses("""
        fn main(abc: u32) { }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 1
    assert len(allocations.colors) == 0
    assert len(allocations.spills) == 0


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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
    assert len(allocations.spills) == 0

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
            val j: u8 = 0x1a;
            val k: u8 = 0x1b;
            val l: u8 = 0x1c;
            val m: u8 = 0x1d;
            val n: u8 = 0x1e;
            val o: u8 = 0x1f;
            val p: u8 = 0x20;
            val q: u8 = 0x21;
            val r: u8 = 0x22;

            foo(a,b,c);
            foo(d,e,f);
            foo(g,h,i);
            foo(j,k,l);
            foo(m,n,o);
            foo(p,q,r);
        }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 24
    assert len(allocations.colors) == 15

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ParameterAcceptance)

    for idx in range(2, 18):
        assert isinstance(allocations.values[idx], ValueAcceptance)

    for idx in range(18, 24):
        assert isinstance(allocations.values[idx], Calling)

    # colors are assigned backwards
    for idx in range(3, 18):
        assert allocations.colors[idx] == 17 - idx

    # spilled values are not colored
    for idx in range(3):
        assert allocations.spills[idx] == 2 - idx


def can_detect_allocations_with_forced_spill_two_blocks():
    _, analyses = prepare_analyses("""
        asm foo(a@rax: u8, b@rbx: u8, c@rcx: u8)
            clobbers rdi, rsi, rdx, rcx, r8, r9, r10, r11, r12, r13, r14, r15, rbx, rax
        {
        }

        fn main(a: u8, b: u8) {
            foo(a,b, 0x13);
            val c: u8 = 0x14;
            val d: u8 = 0x15;
            foo(a,c,d);
        }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 34
    assert allocations.colors == {1: 10, 18: 10}
    assert allocations.spills == {0: 1, 17: 0}

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ParameterAcceptance)


def can_detect_allocations_with_forced_spill_all_clobbered():
    _, analyses = prepare_analyses("""
        asm foo(a@rax: u8, b@rbx: u8, c@rcx: u8)
            clobbers rdi, rsi, rdx, rcx, r8, r9, r10, r11, r12, r13, r14, r15, rbx, rax, rbp
        {
        }

        fn main(a: u8, b: u8) {
            foo(a,b, 0x13);
        }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 18
    assert len(allocations.colors) == 0
    assert allocations.spills == {0: 1, 1: 0}

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ParameterAcceptance)


def can_detect_allocations_with_value_surviving_a_call():
    _, analyses = prepare_analyses("""
        asm foo() clobbers rdi { }
        fn main(abc: u8) { val x: u8 = abc; foo(); val y: u8 = x; }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 5
    assert len(allocations.colors) == 2
    assert len(allocations.spills) == 0

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ValueAcceptance)
    assert isinstance(allocations.values[2], Calling)
    assert isinstance(allocations.values[3], CallingClobber)
    assert isinstance(allocations.values[4], ValueAcceptance)

    # colors are assigned backwards
    assert allocations.colors[0] == 0
    assert allocations.colors[1] == 1


def can_detect_allocations_with_value_surviving_a_call_colliding():
    _, analyses = prepare_analyses("""
        asm foo() clobbers rdi { }
        fn main(abc: u8) { val x: u8 = abc; foo(); val y: u8 = x; val z: u8 = abc; }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 1
    _, allocations = analyses.allocations.peak()

    assert len(allocations.values) == 6
    assert len(allocations.colors) == 2
    assert len(allocations.spills) == 0

    assert isinstance(allocations.values[0], ParameterAcceptance)
    assert isinstance(allocations.values[1], ValueAcceptance)
    assert isinstance(allocations.values[2], Calling)
    assert isinstance(allocations.values[3], CallingClobber)
    assert isinstance(allocations.values[4], ValueAcceptance)
    assert isinstance(allocations.values[5], ValueAcceptance)

    # colors are assigned backwards
    assert allocations.colors[0] == 2
    assert allocations.colors[1] == 1


def can_detect_allocations_with_value_surviving_a_call_of_regular_function():
    _, analyses = prepare_analyses("""
        fn foo() { }
        fn main(abc: u8) { val x: u8 = abc; foo(); val y: u8 = x; }
    """)

    assert analyses.allocations is not None
    assert analyses.allocations.size() == 2
    _, allocations = analyses.allocations.peak()

    for allocations in analyses.allocations.values():
        if len(allocations.values) == 0:
            continue

        assert len(allocations.values) == 13
        assert len(allocations.colors) == 2
        assert len(allocations.spills) == 0

        assert isinstance(allocations.values[0], ParameterAcceptance)
        assert isinstance(allocations.values[1], ValueAcceptance)
        assert isinstance(allocations.values[2], Calling)
        assert isinstance(allocations.values[12], ValueAcceptance)

        for idx in range(3, 12):
            assert isinstance(allocations.values[idx], CallingClobber)

        # colors are assigned backwards
        assert allocations.colors[0] == 0
        assert allocations.colors[1] == 9
