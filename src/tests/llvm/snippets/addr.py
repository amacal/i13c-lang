from tests.llvm.snippets import prepare_main


def can_lower_lea_reg64_addr_disp0():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx]",
    ]


def can_lower_lea_reg64_addr_with_positive_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx + 0x00001234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx + 0x00001234]",
    ]


def can_lower_lea_reg64_addr_with_negative_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx - 0x00001234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx - 0x00001234]",
    ]


def can_lower_lea_reg32_addr_disp0():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea eax, [rbx]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea eax, [rbx]",
    ]


def can_lower_lea_reg32_addr_with_positive_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea eax, [rbx + 0x00001234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea eax, [rbx + 0x00001234]",
    ]


def can_lower_lea_reg32_addr_with_negative_disp32():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea eax, [rbx - 0x00001234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea eax, [rbx - 0x00001234]",
    ]
