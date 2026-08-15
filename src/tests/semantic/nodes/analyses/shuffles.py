from i13c.semantic.typing.analyses.shuffles import ShuffleExchange, ShuffleMove
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_shuffles_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 0


def can_detect_shuffles_with_asm_callsite_using_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) { }
        fn main() { foo(0x42); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 0


def can_detect_shuffles_with_asm_callsite_using_parameter():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { foo(abc); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 1

    assert isinstance(shuffles.callsites[0].moves[0], ShuffleMove)
    assert shuffles.callsites[0].moves[0].src == b"rdi"
    assert shuffles.callsites[0].moves[0].dst == b"rax"


def can_detect_shuffles_with_asm_callsite_using_value():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main() { val abc: u8 = 0x42; foo(abc); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 1

    assert isinstance(shuffles.callsites[0].moves[0], ShuffleMove)
    assert shuffles.callsites[0].moves[0].src == b"rdi"
    assert shuffles.callsites[0].moves[0].dst == b"rax"


def can_detect_shuffles_with_asm_callsite_with_correct_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rsi: u8, y@rdi: u8) { }
        fn main(x: u8, y: u8) { foo(x, y); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 0


def can_detect_shuffles_with_asm_callsite_with_inverted_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rsi: u8, y@rdi: u8) { }
        fn main(x: u8, y: u8) { foo(y, x); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 1

    assert isinstance(shuffles.callsites[0].moves[0], ShuffleExchange)
    assert shuffles.callsites[0].moves[0].src == b"rdi"
    assert shuffles.callsites[0].moves[0].dst == b"rsi"


def can_detect_shuffles_with_asm_callsite_with_shifted_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(x: u8, y: u8, z: u8) { foo(y, z); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 2

    assert isinstance(shuffles.callsites[0].moves[0], ShuffleMove)
    assert shuffles.callsites[0].moves[0].src == b"rsi"
    assert shuffles.callsites[0].moves[0].dst == b"rax"

    assert isinstance(shuffles.callsites[0].moves[1], ShuffleMove)
    assert shuffles.callsites[0].moves[1].src == b"rdi"
    assert shuffles.callsites[0].moves[1].dst == b"rbx"


def can_detect_shuffles_with_asm_callsite_with_three_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8, y@rsi: u8, z@rdx: u8) { }
        fn main(x: u8, y: u8, z: u8) { foo(x, z, y); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 2

    assert isinstance(shuffles.callsites[0].moves[0], ShuffleExchange)
    assert shuffles.callsites[0].moves[0].src == b"rdx"
    assert shuffles.callsites[0].moves[0].dst == b"rdi"

    assert isinstance(shuffles.callsites[0].moves[1], ShuffleExchange)
    assert shuffles.callsites[0].moves[1].src == b"rdx"
    assert shuffles.callsites[0].moves[1].dst == b"rsi"


def can_detect_shuffles_with_asm_callsite_with_same_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8, y@rsi: u8, z@rdx: u8) { }
        fn main(x: u8) { foo(x, x, x); }
    """)

    assert analyses.shuffles is not None
    assert analyses.shuffles.size() == 1
    _, shuffles = analyses.shuffles.peak()

    assert len(shuffles.callsites) == 1
    assert len(shuffles.callsites[0].moves) == 2

    assert isinstance(shuffles.callsites[0].moves[0], ShuffleMove)
    assert shuffles.callsites[0].moves[0].src == b"rdi"
    assert shuffles.callsites[0].moves[0].dst == b"rsi"

    assert isinstance(shuffles.callsites[0].moves[1], ShuffleMove)
    assert shuffles.callsites[0].moves[1].src == b"rdi"
    assert shuffles.callsites[0].moves[1].dst == b"rdx"
