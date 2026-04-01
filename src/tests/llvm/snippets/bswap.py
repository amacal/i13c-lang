from tests.llvm.snippets import prepare_main


def can_lower_bswap_reg64_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { bswap rax; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "bswap rax",
    ]


def can_lower_bswap_reg32_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { bswap eax; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "bswap eax",
    ]
