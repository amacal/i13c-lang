from tests.syntax.parsing import reject_program


def can_reject_address_with_invalid_literal_as_offset():
    code, diagnostics = reject_program(
        """
            asm main() { mov [rax + 0x123]; }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")


def can_reject_snippet_parameter_with_invalid_literal_as_range_lower_bound():
    code, diagnostics = reject_program(
        """
            asm main(value@rdi: u8[0x123..0x20]) { }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")


def can_reject_snippet_parameter_with_invalid_literal_as_range_upper_bound():
    code, diagnostics = reject_program(
        """
            asm main(value@rdi: u8[0x10..0x123]) { }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")


def can_reject_function_parameter_with_invalid_literal_as_range_lower_bound():
    code, diagnostics = reject_program(
        """
            fn main(value: u8[0x123..0x20]) { }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")


def can_reject_function_parameter_with_invalid_literal_as_range_upper_bound():
    code, diagnostics = reject_program(
        """
            fn main(value: u8[0x10..0x123]) { }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")


def can_reject_assembly_instruction_with_invalid_literal_as_immediate():
    code, diagnostics = reject_program(
        """
            asm main() { mov rax, 0x123; }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")


def can_reject_function_call_with_invalid_literal_as_argument():
    code, diagnostics = reject_program(
        """
            fn main() { exit(0x123); }
        """
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == "E2004"
    assert diagnostic.ref.offset == code.data.find(b"0x123")
