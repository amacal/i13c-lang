from typing import List

from i13c import diag, err
from i13c.sem.analysis import Analysis
from i13c.sem.graph import Graph


def validate_called_symbol_termination(
    graph: Graph,
    analysis: Analysis,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, terminal in analysis.is_terminal.items():
        if not terminal:
            continue

        for sid in analysis.function_exits.get(fid):
            if cid := graph.edges.statement_calls.find_by_id(sid):
                if callees := graph.edges.call_targets.get(cid):
                    if not analysis.is_terminal.find_by_id(callees[0]):
                        if call := graph.nodes.calls.find_by_id(cid):
                            diagnostics.append(
                                err.report_e3010_callee_is_non_terminal(
                                    call.ref,
                                    call.name,
                                )
                            )

    return diagnostics
