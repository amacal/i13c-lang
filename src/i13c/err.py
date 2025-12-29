from typing import List, Set, Union

from i13c import diag, src

ERROR_1000 = "E1000"  # Unrecognized token
ERROR_1001 = "E1001"  # Unexpected end of file
ERROR_1002 = "E1002"  # Unexpected value

ERROR_2000 = "E2000"  # Unexpected end of tokens
ERROR_2001 = "E2001"  # Unexpected token
ERROR_2002 = "E2002"  # Unexpected keyword
ERROR_2003 = "E2003"  # Function flag already specified

ERROR_3000 = "E3000"  # Unknown mnemonic
ERROR_3001 = "E3001"  # Immediate out of range
ERROR_3002 = "E3002"  # Invalid operand types
ERROR_3003 = "E3003"  # Duplicated parameter bindings
ERROR_3004 = "E3004"  # Duplicated parameter names
ERROR_3005 = "E3005"  # Duplicated clobber registers
ERROR_3006 = "E3006"  # Duplicated function names
ERROR_3007 = "E3007"  # Integer literal out of range
ERROR_3008 = "E3008"  # Called symbol does not exist
ERROR_3009 = "E3009"  # Called symbol is not a snippet
ERROR_3010 = "E3010"  # Function has wrong terminality
ERROR_3011 = "E3011"  # Missing entrypoint function
ERROR_3012 = "E3012"  # Multiple entrypoint functions

ERROR_4000 = "E4000"  # Unsupported mnemonic


def report_e1000_unrecognized_token(offset: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=src.Span(offset=offset, length=1),
        code=ERROR_1000,
        message="Unrecognized token",
    )


def report_e1001_unexpected_end_of_file(offset: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=src.Span(offset=offset, length=1),
        code=ERROR_1001,
        message="Unexpected end of file",
    )


def report_e1002_unexpected_value(offset: int, expected: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=src.Span(offset=offset, length=1),
        code=ERROR_1002,
        message=f"Unexpected value at offset {offset}, expected one of: {list(expected)}",
    )


def report_e2000_unexpected_end_of_tokens(offset: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=src.Span(offset=offset, length=0),
        code=ERROR_2000,
        message=f"Unexpected end of tokens at offset {offset}",
    )


def report_e2001_unexpected_token(
    ref: src.SpanLike, expected: List[int], found: int
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_2001,
        message=f"Unexpected token code {found} at offset {ref.offset}, expected one of: {list(expected)}",
    )


def report_e2002_unexpected_keyword(
    ref: src.SpanLike, expected: Union[List[bytes], Set[bytes]], found: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_2002,
        message=f"Unexpected keyword '{found.decode()}' at offset {ref.offset}, expected one of: {list(expected)}",
    )


def report_e2003_flag_already_specified(
    ref: src.SpanLike, flag: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_2003,
        message=f"Function flag '{flag.decode()}' already specified at offset {ref.offset}",
    )


def report_e3000_unknown_instruction(ref: src.SpanLike) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3000,
        message=f"Unknown instruction mnemonic at offset {ref.offset}",
    )


def report_e3001_immediate_out_of_range(
    ref: src.SpanLike, value: int
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3001,
        message=f"Immediate value {value} out of range at offset {ref.offset}",
    )


def report_e3002_invalid_operand_types(
    ref: src.SpanLike, found: List[str]
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3002,
        message=f"Invalid operand types ({', '.join(found)}) at offset {ref.offset}",
    )


def report_e3003_duplicated_slot_bindings(
    ref: src.SpanLike, found: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3003,
        message=f"Duplicated parameter bindings for ({str(found)}) at offset {ref.offset}",
    )


def report_e3004_duplicated_parameter_names(
    ref: src.SpanLike, found: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3004,
        message=f"Duplicated parameter names for ({str(found)}) at offset {ref.offset}",
    )


def report_e3005_duplicated_snippet_clobbers(
    ref: src.SpanLike, found: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3005,
        message=f"Duplicated clobber registers for ({str(found)}) at offset {ref.offset}",
    )


def report_e3006_duplicated_function_names(
    ref: src.SpanLike, found: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3006,
        message=f"Duplicated function names for ({str(found)}) at offset {ref.offset}",
    )


def report_e3007_integer_literal_out_of_range(
    ref: src.SpanLike, value: int
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3007,
        message=f"Immediate value {value} out of range at offset {ref.offset}",
    )


def report_e3008_called_symbol_exists(
    ref: src.SpanLike, name: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3008,
        message=f"Called symbol does not exist: {str(name)}",
    )


def report_e3009_called_symbol_is_not_a_snippet(
    ref: src.SpanLike, name: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3009,
        message=f"Called symbol is not a snippet: {str(name)}",
    )


def report_e3010_function_has_wrong_terminality(
    ref: src.SpanLike, name: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_3010,
        message=f"Function '{str(name)}' has wrong terminality: does not match declaration",
    )


def report_e3011_missing_entrypoint_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=src.Span(offset=0, length=0),
        code=ERROR_3011,
        message="Missing entrypoint codeblock",
    )


def report_e3012_multiple_entrypoint_functions() -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=src.Span(offset=0, length=0),
        code=ERROR_3012,
        message="Multiple entrypoint codeblocks found",
    )


def report_e4000_unsupported_mnemonic(
    ref: src.SpanLike, name: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        ref=ref,
        code=ERROR_4000,
        message=f"Unsupported mnemonic: {name.decode()}",
    )
