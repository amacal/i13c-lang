from typing import List

from i13c import diag, err, ir, res


def link(unit: ir.Unit) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    blocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []

    for idx, block in enumerate(unit.codeblocks):
        if unit.entry is not None and idx == unit.entry:
            blocks.insert(0, block)
        else:
            blocks.append(block)

    if unit.entry is None:
        diagnostics.append(err.report_e5000_missing_entrypoint_function())

    elif blocks[0].terminal is False:
        diagnostics.append(err.report_e5001_non_terminal_entrypoint_function())

    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ir.Unit(entry=0, codeblocks=blocks))
