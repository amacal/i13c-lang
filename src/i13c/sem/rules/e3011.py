from typing import List

from i13c import diag, err
from i13c.sem.graph import Graph
from i13c.sem.model import SemanticModel


def validate_called_arguments_count(
    graph: Graph,
    model: SemanticModel,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in graph.nodes.calls.items():
        by_name = model.resolver.by_name.get(cid)
        by_arity = model.resolver.by_arity.get(cid)

        # if name existed but arity eliminated everything → mismatch
        if by_name and not by_arity:
            diagnostics.append(
                err.report_e3011_called_argument_count_mismatch(
                    call.ref, len(call.arguments), -1
                )
            )

    return diagnostics
