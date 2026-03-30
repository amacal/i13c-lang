from tests.llvm.snippets import prepare_snippet


def can_lower_shl_imm8_program():
    instructions = prepare_snippet("""
        asm foo() noreturn { shl rax, 0x41; }
        fn main() noreturn { foo(); }
    """)

    assert instructions == [
        "shl rax, 0x00000041",
    ]

def can_lower_shl_cl_program():
    instructions = prepare_snippet("""
        asm foo() noreturn { shl rax, cl; }
        fn main() noreturn { foo(); }
    """)

    assert instructions == [
        "shl rax, cl",
    ]
