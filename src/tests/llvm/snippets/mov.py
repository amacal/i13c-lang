from tests.llvm.snippets import prepare_main


def can_lower_movregimm_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { mov rax, 0x1234; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "mov rax, 0x00001234",
    ]


def can_lower_movregreg_program():
    instructions = prepare_main(
        """
            asm foo() noreturn { mov rax, rbx; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "mov rax, rbx",
    ]


def can_lower_movregimm_with_register_bound_slot():
    instructions = prepare_main(
        """
            asm foo(dst@rax: u64, value@imm: u8) noreturn { mov @dst, @value; }
            fn main() noreturn { foo(0x01, 0x42); }
        """
    )

    assert instructions == [
        "mov rax, 0x00000001",
        "mov rax, 0x00000042",
    ]


def can_lower_movoffimm_program_without_offset():
    instructions = prepare_main(
        """
            asm foo() noreturn { mov [rax], 0x1234; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "mov [rax + 0x00000000], 0x00001234",
    ]


def can_lower_movoffimm_program_with_positive_offset():
    instructions = prepare_main(
        """
            asm foo() noreturn { mov [rax + 0x10], 0x1234; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "mov [rax + 0x00000010], 0x00001234",
    ]


def can_lower_movoffimm_program_with_negative_offset():
    instructions = prepare_main(
        """
            asm foo() noreturn { mov [rax - 0x10], 0x1234; }
            fn main() noreturn { foo(); }
        """
    )

    assert instructions == [
        "mov [rax - 0x00000010], 0x00001234",
    ]


# def can_lower_movregoff_program_without_offset():
#     instructions = prepare_main(
#         """
#             asm foo() noreturn { mov rax, [rbx]; }
#             fn main() noreturn { foo(); }
#         """
#     )

#     assert instructions == [
#         "mov rax, qword ptr [rbx]",
#     ]
