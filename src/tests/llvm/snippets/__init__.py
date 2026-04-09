from tests.llvm import prepare_main


def can_lower_multiple_callsites():
    instructions = prepare_main("""
        fn main() noreturn { foo(); bar(); }
        asm foo() { mov rax, 0x01; }
        asm bar() noreturn { syscall; }
    """)

    assert instructions == [
        "mov rax, 0x01",
        "syscall",
    ]
