from typing import List

from i13c import ast, diag, err
from i13c.sem.graph import Graph
from i13c.sem.model import SemanticModel


def validate_called_symbol_is_asm(
    graph: Graph,
    model: SemanticModel,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in graph.nodes.calls.items():
        fids = model.resolver.by_type.get(cid)

        # if nothing is callable, another rule will complain
        if not fids:
            continue

        for fid in fids:
            function = graph.nodes.functions.get_by_id(fid)
            if not isinstance(function, ast.Snippet):
                diagnostics.append(
                    err.report_e3009_called_symbol_is_asm(call.ref, call.name)
                )

                break

    return diagnostics
