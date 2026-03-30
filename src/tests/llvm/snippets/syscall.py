from tests.llvm.snippets import prepare_snippet


def can_lower_syscall_program():
    instructions = prepare_snippet("""
        asm foo() noreturn { syscall; }
        fn main() noreturn { foo(); }
    """)

    assert instructions == [
        "syscall",
    ]
