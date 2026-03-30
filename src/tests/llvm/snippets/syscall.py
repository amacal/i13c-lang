from tests.llvm.snippets import prepare_main


def can_lower_syscall_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { syscall; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "syscall",
    ]
