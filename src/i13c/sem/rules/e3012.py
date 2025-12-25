from typing import List

from i13c import diag, err
from i13c.sem.nodes import Call, Function


def fits(stmt: Call, fn: Function) -> bool:
    for arg, param in zip(stmt.arguments, fn.parameters):
        val = arg.value.value
        typ = param.type.name

        if typ == b"u8" and not (0 <= val <= 0xFF):
            return False
        if typ == b"u16" and not (0 <= val <= 0xFFFF):
            return False
        if typ == b"u32" and not (0 <= val <= 0xFFFFFFFF):
            return False
        if typ == b"u64" and not (0 <= val <= 0xFFFFFFFFFFFFFFFF):
            return False

    return True


def validate_called_arguments_types(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fn in functions:
        for stmt in fn.body:
            if not isinstance(stmt, Call):
                continue

            # snapshot before filtering
            before = list(stmt.candidates)

            # keep only functions with matching argument types
            stmt.candidates = [fn for fn in stmt.candidates if fits(stmt, fn)]

            # name matched but types eliminated all
            if before and not stmt.candidates:
                diagnostics.append(
                    err.report_e3012_called_argument_type_mismatch(
                        stmt.ref,
                        -1,
                        b"<unknown>",
                        b"<unknown>",
                    )
                )

    return diagnostics
