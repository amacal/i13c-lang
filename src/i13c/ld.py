from typing import List

from i13c import diag, ir, res


def link(
    blocks: List[ir.CodeBlock],
) -> res.Result[List[ir.CodeBlock], List[diag.Diagnostic]]:
    linked: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []

    for block in blocks:
        if block.label == b"main":
            linked.insert(0, block)
        else:
            linked.append(block)

    if linked[0].label != b"main":
        diagnostics.append(report_missing_main_function())

    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(linked)


def report_missing_main_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=0,
        code="X001",
        message="Missing entrypoint 'main'",
    )
