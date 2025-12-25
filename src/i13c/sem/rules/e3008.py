from typing import List

from i13c import diag, err
from i13c.sem.graph import Graph
from i13c.sem.model import SemanticModel


def validate_called_symbol_exists(
    graph: Graph,
    model: SemanticModel,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in graph.nodes.calls.items():
        if not model.resolver.by_name.get(cid):
            diagnostics.append(
                err.report_e3008_called_symbol_exists(call.ref, call.name)
            )

    return diagnostics
