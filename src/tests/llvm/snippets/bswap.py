from tests.llvm.snippets import prepare_main


def can_lower_bswap_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { bswap rax; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "bswap rax",
    ]
