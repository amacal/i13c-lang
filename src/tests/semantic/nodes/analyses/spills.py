from i13c.semantic.typing.analyses.spills import SpillReg, SpillScratch
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_spills_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 2
    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0


def can_detect_no_spills_on_callsite_with_a_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) { }
        fn main() { foo(0x42); }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 3
    assert len(spills.spills[1]) == 0

    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0


def can_detect_no_spills_on_parameter_put_in_reg():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax { }

        fn main(abc: u8) { foo(abc); }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 3
    assert len(spills.spills[1]) == 0

    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0


def can_detect_no_spills_on_parameter_put_in_slot():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main(abc: u8) { foo(abc); }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 3
    assert len(spills.spills[1]) == 0

    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0


def can_detect_one_spill_on_value_of_literal_put_in_reg():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax { }

        fn main() { val abc: u8 = 0x01; foo(abc); }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 4
    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0

    assert len(spills.spills[1]) == 0
    assert len(spills.spills[2]) == 0


def can_detect_one_spill_on_value_of_literal_put_in_slot():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main() { val abc: u8 = 0x01; foo(abc); }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 4
    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0

    assert len(spills.spills[1]) == 1
    assert len(spills.spills[2]) == 0

    assert isinstance(spills.spills[1][0], SpillScratch)
    assert spills.spills[1][0].slot == 0
    assert spills.spills[1][0].src == b"r11"


def can_detect_one_spill_on_value_of_variable_put_in_slot():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main(x: u8) { val abc: u8 = x; foo(abc); }
    """)

    assert analyses.spills is not None
    assert analyses.spills.size() == 1
    _, spills = analyses.spills.peek()

    assert len(spills.spills) == 4
    assert len(spills.spills[spills.entry]) == 0
    assert len(spills.spills[spills.exit]) == 0

    assert len(spills.spills[1]) == 1
    assert len(spills.spills[2]) == 0

    assert isinstance(spills.spills[1][0], SpillReg)
    assert spills.spills[1][0].slot == 0
    assert spills.spills[1][0].src == b"rdi"
