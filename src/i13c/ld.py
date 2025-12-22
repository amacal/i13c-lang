from typing import List

from i13c import diag, ir, res


def link(unit: ir.Unit) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    blocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []

    for block in unit.codeblocks:
        if block.label == b"main":
            blocks.insert(0, block)
        else:
            blocks.append(block)

    if blocks[0].label != b"main":
        diagnostics.append(report_missing_main_function())

    if blocks[0].terminal is False:
        diagnostics.append(report_non_terminal_main_function())

    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ir.Unit(symbols=set(), codeblocks=blocks))


def report_missing_main_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=0,
        code="X001",
        message="Missing entrypoint 'main'",
    )


def report_non_terminal_main_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=0,
        code="X002",
        message="The entrypoint 'main' must be terminal",
    )
