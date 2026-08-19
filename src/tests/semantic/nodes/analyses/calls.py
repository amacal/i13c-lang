
from i13c.semantic.typing.analyses.llvm import Call, Exchange, Move
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_calls_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 0


def can_detect_calls_with_asm_callsite_using_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) { }
        fn main() { foo(0x42); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 1
    assert isinstance(call.instructions[0], Call)

    assert call.instructions[0].target == asmlet.id


def can_detect_calls_with_asm_callsite_using_parameter():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { foo(abc); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 2
    assert isinstance(call.instructions[0], Move)
    assert isinstance(call.instructions[1], Call)

    assert str(call.instructions[0].variant[0]) == "rax"
    assert str(call.instructions[0].variant[1]) == "rdi"

    assert call.instructions[1].target == asmlet.id


def can_detect_calls_with_asm_callsite_using_value():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main() { val abc: u8 = 0x42; foo(abc); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 2
    assert isinstance(call.instructions[0], Move)
    assert isinstance(call.instructions[1], Call)

    assert str(call.instructions[0].variant[0]) == "rax"
    assert str(call.instructions[0].variant[1]) == "rdi"

    assert call.instructions[1].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_correct_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rsi: u8, y@rdi: u8) { }
        fn main(x: u8, y: u8) { foo(x, y); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 1
    assert isinstance(call.instructions[0], Call)

    assert call.instructions[0].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_inverted_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rsi: u8, y@rdi: u8) { }
        fn main(x: u8, y: u8) { foo(y, x); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 2
    assert isinstance(call.instructions[0], Exchange)
    assert isinstance(call.instructions[1], Call)

    assert str(call.instructions[0].dst) == "rsi"
    assert str(call.instructions[0].src) == "rdi"

    assert call.instructions[1].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_shifted_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8, y@rbx: u8) { }
        fn main(x: u8, y: u8, z: u8) { foo(y, z); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 3
    assert isinstance(call.instructions[0], Move)
    assert isinstance(call.instructions[1], Move)
    assert isinstance(call.instructions[2], Call)

    assert str(call.instructions[0].variant[0]) == "rax"
    assert str(call.instructions[0].variant[1]) == "rsi"

    assert str(call.instructions[1].variant[0]) == "rbx"
    assert str(call.instructions[1].variant[1]) == "rdi"

    assert call.instructions[2].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_three_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8, y@rsi: u8, z@rdx: u8) { }
        fn main(x: u8, y: u8, z: u8) { foo(x, z, y); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 3
    assert isinstance(call.instructions[0], Exchange)
    assert isinstance(call.instructions[1], Exchange)
    assert isinstance(call.instructions[2], Call)

    assert str(call.instructions[0].src) == "rdx"
    assert str(call.instructions[0].dst) == "rdi"

    assert str(call.instructions[1].src) == "rdx"
    assert str(call.instructions[1].dst) == "rsi"

    assert call.instructions[2].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_same_params():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8, y@rsi: u8, z@rdx: u8) { }
        fn main(x: u8) { foo(x, x, x); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 3
    assert isinstance(call.instructions[0], Move)
    assert isinstance(call.instructions[1], Move)
    assert isinstance(call.instructions[2], Call)

    assert str(call.instructions[0].variant[0]) == "rsi"
    assert str(call.instructions[0].variant[1]) == "rdi"

    assert str(call.instructions[1].variant[0]) == "rdx"
    assert str(call.instructions[1].variant[1]) == "rdi"

    assert call.instructions[2].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8) { }
        fn main() { foo(0x05); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 2
    assert isinstance(call.instructions[0], Move)
    assert isinstance(call.instructions[1], Call)

    assert str(call.instructions[0].variant[0]) == "rdi"
    assert str(call.instructions[0].variant[1]) == "0x05"

    assert call.instructions[1].target == asmlet.id


def can_detect_calls_with_asm_callsite_with_spilled_param():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main(x: u8) { foo(x); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peek()

    assert len(call.instructions) == 2
    assert isinstance(call.instructions[0], Move)
    assert isinstance(call.instructions[1], Call)

    assert str(call.instructions[0].variant[0]) == "rax"
    assert str(call.instructions[0].variant[1]) == "#0"

    assert call.instructions[1].target == asmlet.id
