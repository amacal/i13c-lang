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


def can_lower_shl_reg64_imm8_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { shl rax, 0x41; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "shl rax, 0x41",
    ]


def can_lower_shl_reg32_imm8_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { shl eax, 0x41; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "shl eax, 0x41",
    ]


def can_lower_shl_reg16_imm8_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { shl ax, 0x41; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "shl ax, 0x41",
    ]


def can_lower_shl_reg8_imm8_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { shl al, 0x41; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "shl al, 0x41",
    ]


def can_lower_shl_reg64_cl_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { shl rax, cl; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "shl rax, cl",
    ]
