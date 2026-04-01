from tests.llvm.snippets import prepare_main


def can_lower_lea_reg64_addr64_disp0():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx + 0x00000000]",
    ]


def can_lower_lea_reg64_addr64_with_positive_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx + 0x1234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx + 0x00001234]",
    ]


def can_lower_lea_reg64_addr64_with_negative_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx - 0x1234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx - 0x00001234]",
    ]


def can_lower_lea_reg32_addr64_disp0():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea eax, [rbx]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea eax, [rbx + 0x00000000]",
    ]


def can_lower_lea_reg32_addr64_with_positive_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea eax, [rbx + 0x1234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea eax, [rbx + 0x00001234]",
    ]


def can_lower_lea_reg32_addr64_with_negative_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea eax, [rbx - 0x1234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea eax, [rbx - 0x00001234]",
    ]
