from typing import List

from i13c.core import diagnostics
from i13c.syntax.source import Span, SpanLike

ERROR_2000 = "E2000"  # Unexpected end of tokens
ERROR_2001 = "E2001"  # Unexpected token
ERROR_2002 = "E2002"  # Unexpected keyword
ERROR_2003 = "E2003"  # Function flag already specified

ERROR_3000 = "E3000"  # Unknown mnemonic
ERROR_3001 = "E3001"  # Invalid type ranges
ERROR_3002 = "E3002"  # Invalid operand types
ERROR_3003 = "E3003"  # Duplicated parameter bindings
ERROR_3004 = "E3004"  # Duplicated parameter names
ERROR_3005 = "E3005"  # Duplicated clobber registers
ERROR_3006 = "E3006"  # Duplicated function names
ERROR_3007 = "E3007"  # Called symbol has no matching overload
ERROR_3008 = "E3008"  # Called symbol does not exist
ERROR_3010 = "E3010"  # Function has wrong terminality
ERROR_3011 = "E3011"  # Missing entrypoint function or snippet
ERROR_3012 = "E3012"  # Multiple entrypoint functions

ERROR_4000 = "E4000"  # Unsupported mnemonic

def report_e3000_unknown_instruction(ref: SpanLike) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3000,
        message=f"Unknown instruction mnemonic at offset {ref.offset}",
    )


def report_e3001_invalid_type_ranges(
    ref: SpanLike, lower: int, upper: int
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3001,
        message=f"Invalid type ranges [{lower}..{upper}] at offset {ref.offset}",
    )


def report_e3002_invalid_operand_types(
    ref: SpanLike, found: List[str]
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3002,
        message=f"Invalid operand types ({', '.join(found)}) at offset {ref.offset}",
    )


def report_e3003_duplicated_slot_bindings(
    ref: SpanLike, found: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3003,
        message=f"Duplicated parameter bindings for ({str(found)}) at offset {ref.offset}",
    )


def report_e3004_duplicated_parameter_names(
    ref: SpanLike, found: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3004,
        message=f"Duplicated parameter names for ({str(found)}) at offset {ref.offset}",
    )


def report_e3005_duplicated_snippet_clobbers(
    ref: SpanLike, found: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3005,
        message=f"Duplicated clobber registers for ({str(found)}) at offset {ref.offset}",
    )


def report_e3006_duplicated_function_names(
    ref: SpanLike, found: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3006,
        message=f"Duplicated function names for ({str(found)}) at offset {ref.offset}",
    )


def report_e3007_no_matching_overload(
    ref: SpanLike, name: bytes, candidates: List[str]
) -> diagnostics.Diagnostic:
    template = (
        "Called symbol '{name}' has no matching overload.\n"
        "Tried candidates:\n{candidates}"
    )

    args = dict(
        name=name.decode(),
        candidates="\n".join([f"  - {c}" for c in candidates]),
    )

    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3007,
        message=template.format(**args),
    )


def report_e3008_called_symbol_missing(
    ref: SpanLike, name: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3008,
        message=f"Called symbol does not exist: {str(name)}",
    )


def report_e3010_function_has_wrong_terminality(
    ref: SpanLike, name: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_3010,
        message=f"Function '{str(name)}' has wrong terminality: does not match declaration",
    )


def report_e3011_missing_entrypoint_function() -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=Span(offset=0, length=0),
        code=ERROR_3011,
        message="Missing entrypoint function or snippet named 'main'",
    )


def report_e3012_multiple_entrypoint_functions() -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=Span(offset=0, length=0),
        code=ERROR_3012,
        message="Multiple entrypoint codeblocks found",
    )


def report_e4000_unsupported_mnemonic(
    ref: SpanLike, name: bytes
) -> diagnostics.Diagnostic:
    return diagnostics.Diagnostic(
        ref=ref,
        code=ERROR_4000,
        message=f"Unsupported mnemonic: {name.decode()}",
    )
