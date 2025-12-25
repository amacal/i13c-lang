from typing import List

from i13c import diag, err
from i13c.sem.graph import Graph
from i13c.sem.model import SemanticModel


def validate_called_symbol_termination(
    graph: Graph,
    model: SemanticModel,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, terminal in model.analysis.is_terminal.items():
        if not terminal:
            continue

        for sid in model.analysis.function_exits.get(fid):
            if cid := graph.edges.statement_calls.find_by_id(sid):
                callees = model.resolver.by_type.get(cid)

                # unresolved calls handled elsewhere
                if not callees:
                    continue

                for callee in callees:
                    if not model.analysis.is_terminal.find_by_id(callee):
                        # find the call node
                        call = graph.nodes.calls.get_by_id(cid)

                        diagnostics.append(
                            err.report_e3010_callee_is_non_terminal(call.ref, call.name)
                        )

                        break

    return diagnostics
