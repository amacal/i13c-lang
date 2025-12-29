from typing import List, Optional, Set

from i13c import diag, ir, res


def layout(unit: ir.Unit) -> List[int]:
    out: List[int] = []
    visited: Set[int] = set()
    node: Optional[int] = unit.entry

    # follow fallthrough chain
    while node is not None and node not in visited:
        visited.add(node)
        out.append(node)

        # find the terminator
        terminator = unit.codeblocks[node].terminator

        # follow fallthroughs only
        if isinstance(terminator, ir.FallThrough):
            node = terminator.target
        else:
            node = None

    # should be good enough for now
    assert len(out) == len(unit.codeblocks)

    # ordering
    return out


def link(unit: ir.Unit) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    blocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []

    for idx in layout(unit):
        blocks.append(unit.codeblocks[idx])

    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ir.Unit(entry=0, codeblocks=blocks))
