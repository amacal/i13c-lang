from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_frames_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.frames is not None
    assert analyses.frames.size() == 1
    _, frames = analyses.frames.peek()

    assert len(frames.moved) == 0
    assert len(frames.spill) == 0
    assert len(frames.saved) == 0
    assert frames.slots == 0


def can_detect_frames_with_a_parameter():
    _, analyses = prepare_analyses("""
        fn main(v: u16) { }
    """)

    assert analyses.frames is not None
    assert analyses.frames.size() == 1
    _, frames = analyses.frames.peek()

    assert len(frames.moved) == 0
    assert len(frames.spill) == 0
    assert len(frames.saved) == 0
    assert frames.slots == 0


def can_detect_frames_with_a_parameter_move():
    _, analyses = prepare_analyses("""
        asm foo(v@rax: u16)
          clobbers rdi, rsi, rdx, rcx, r8, r9, r10, r11, r12, r13, r14, r15, rbx, rax
        { }

        fn main(v: u16) { foo(v); }
    """)

    assert analyses.frames is not None
    assert analyses.frames.size() == 1
    _, frames = analyses.frames.peek()

    assert len(frames.moved) == 1
    assert len(frames.spill) == 0
    assert len(frames.saved) == 6
    assert frames.slots == 0

    assert frames.moved[0].src == b"rdi"
    assert frames.moved[0].dst == b"rbp"


def can_detect_frames_with_a_parameter_spill():
    _, analyses = prepare_analyses("""
        asm foo(v@rax: u16)
          clobbers rdi, rsi, rdx, rcx, r8, r9, r10, r11, r12, r13, r14, r15, rbx, rax, rbp
        { }

        fn main(v: u16) { foo(v); }
    """)

    assert analyses.frames is not None
    assert analyses.frames.size() == 1
    _, frames = analyses.frames.peek()

    assert len(frames.moved) == 0
    assert len(frames.spill) == 1
    assert len(frames.saved) == 6
    assert frames.slots == 1

    assert frames.spill[0].name == b"rdi"
    assert frames.spill[0].slot == 0


def can_detect_frames_with_a_parameter_spill_and_value():
    _, analyses = prepare_analyses("""
        asm foo(v@rax: u16, w@rsi: u16)
          clobbers rdi, rsi, rdx, rcx, r8, r9, r10, r11, r12, r13, r14, r15, rbx, rax, rbp
        { }

        fn main(v: u16) { val x: u16 = 0x01; foo(v, x); }
    """)

    assert analyses.frames is not None
    assert analyses.frames.size() == 1
    _, frames = analyses.frames.peek()

    assert len(frames.moved) == 0
    assert len(frames.spill) == 1
    assert len(frames.saved) == 6
    assert frames.slots == 2

    assert frames.spill[0].name == b"rdi"
    assert frames.spill[0].slot == 1


def can_detect_frames_with_a_call_to_regular_function():
    _, analyses = prepare_analyses("""
        fn foo(x: u16, y: u16) { }
        fn main(v: u16) { foo(v,v); }
    """)

    assert analyses.frames is not None
    assert analyses.frames.size() == 2

    for frames in analyses.frames.values():
        if frames.moved:
            assert len(frames.moved) == 1
            assert len(frames.spill) == 0
            assert len(frames.saved) == 1
            assert frames.slots == 0

            assert frames.moved[0].src == b"rdi"
            assert frames.moved[0].dst == b"rbx"
