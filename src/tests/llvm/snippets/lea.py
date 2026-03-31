from tests.llvm.snippets import prepare_main


def can_lower_lea_reg_address_without_offset():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx + 0x00000000]",
    ]


def can_lower_lea_reg_address_with_positive_offset():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx + 0x1234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx + 0x00001234]",
    ]


def can_lower_lea_reg_address_with_negative_offset():
    instructions = prepare_main(
        """
            asm foo() noreturn { lea rax, [rbx - 0x1234]; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "lea rax, [rbx - 0x00001234]",
    ]
