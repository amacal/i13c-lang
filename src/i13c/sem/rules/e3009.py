from typing import List

from i13c import ast, diag, err
from i13c.sem.analysis import Analysis
from i13c.sem.graph import Graph


def validate_called_symbol_is_asm(
    graph: Graph,
    analysis: Analysis,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in graph.nodes.calls.id_to_node.items():
        if fids := graph.edges.call_targets.get(cid):
            if target := graph.nodes.functions.find_by_id(fids[0]):
                if not isinstance(target, ast.AsmFunction):
                    diagnostics.append(
                        err.report_e3009_called_symbol_is_asm(
                            call.ref,
                            call.name,
                        )
                    )

    return diagnostics
