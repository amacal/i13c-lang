from typing import List

from i13c import diag, err
from i13c.sem import rel


def validate_called_symbol_termination(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, terminal in relationships.analysis.is_terminal.items():
        if not terminal:
            continue

        for sid in relationships.analysis.function_exits.get(fid):
            if cid := relationships.edges.statement_calls.find_by_id(sid):
                if callee := relationships.edges.call_targets.find_by_id(cid):
                    if not relationships.analysis.is_terminal.find_by_id(callee):
                        if call := relationships.nodes.calls.find_by_id(cid):
                            diagnostics.append(
                                err.report_e3010_callee_is_non_terminal(
                                    call.ref,
                                    call.name,
                                )
                            )

    return diagnostics
