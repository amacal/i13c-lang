
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_fnlets_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.fnlets is not None
    assert analyses.fnlets.size() == 1
    _, fnlet = analyses.fnlets.peek()

    # PROLOG and EPILOG each get their own block
    assert len(fnlet.blocks) == 2
    assert len(fnlet.blocks[0].instructions) == 1
    assert len(fnlet.blocks[1].instructions) == 1


def can_detect_fnlets_pure_assign_and_call():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main() { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.fnlets is not None
    assert analyses.fnlets.size() == 1
    _, fnlet = analyses.fnlets.peek()

    # a block boundary falls at PROLOG, the assign, the call, and EPILOG
    assert len(fnlet.blocks) == 4
    assert len(fnlet.blocks[0].instructions) == 1
    assert len(fnlet.blocks[1].instructions) == 1
    assert len(fnlet.blocks[2].instructions) == 1
    assert len(fnlet.blocks[3].instructions) == 1


def can_detect_fnlets_assign_with_spills():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main() { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.fnlets is not None
    assert analyses.fnlets.size() == 1
    _, fnlet = analyses.fnlets.peek()

    # spilling is resolved later during register allocation, not here
    assert len(fnlet.blocks) == 4
    assert len(fnlet.blocks[0].instructions) == 1
    assert len(fnlet.blocks[1].instructions) == 1
    assert len(fnlet.blocks[2].instructions) == 1
    assert len(fnlet.blocks[3].instructions) == 1
