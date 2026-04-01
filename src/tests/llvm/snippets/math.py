from tests.llvm.snippets import prepare_main


def can_lower_add_reg_imm32_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { add rax, 0x12345678; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "add rax, 0x12345678",
    ]


def can_lower_add_reg_reg_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { add rax, rbx; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "add rax, rbx",
    ]
