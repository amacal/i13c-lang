from typing import List

from i13c import diag, ir, res


def link(unit: ir.Unit) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    blocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []

    for idx, block in enumerate(unit.codeblocks):
        if unit.entry is not None and idx == unit.entry:
            blocks.insert(0, block)
        else:
            blocks.append(block)

    if unit.entry is None:
        diagnostics.append(report_missing_entrpoint_function())

    elif blocks[0].terminal is False:
        diagnostics.append(report_non_terminal_entrypoint_function())

    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ir.Unit(entry=0, codeblocks=blocks))


def report_missing_entrpoint_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=0,
        code="X001",
        message="Missing entrypoint codeblock",
    )


def report_non_terminal_entrypoint_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=0,
        code="X002",
        message="The entrypoint codeblock must be terminal",
    )
