
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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]

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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


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
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


def can_detect_calls_when_used_in_assignment():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8) -> u16@rax clobbers rax { }
        fn main(x: u8) { val v: u16 = foo(x); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]

    assert call.instructions[0].args


def can_detect_calls_with_asm_callsite_with_spilled_param():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main(x: u8) { foo(x); val v: u8 = x; }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    asmlet, _ = analyses.asmlets.peek()

    assert call.listing() == [
        f"call {asmlet.identify(1)}",
    ]


def can_detect_calls_collecting_output_from_declared_register():
    _, analyses = prepare_analyses("""
        asm foo() -> u64@rdx clobbers rdx { }
        fn main() { val v: u64 = foo(); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert len(call.instructions) == 1
    instr = call.instructions[0]

    # the output is collected from rdx as declared, not from the default rax
    assert {dst: src.name for dst, src in instr.outs.items()} == {b"rdx": b"v1"}


def can_detect_calls_not_duplicating_a_declared_result_clobber():
    _, analyses = prepare_analyses("""
        asm foo() -> u64@rax clobbers rax { }
        fn main() { val v: u64 = foo(); }
    """)

    assert analyses.calls is not None
    assert analyses.calls.size() == 1
    _, call = analyses.calls.peek()

    assert len(call.instructions) == 1
    instr = call.instructions[0]

    # the result register must be declared as a clobber, and it's listed once
    assert instr.clobbers == [b"rax"]
