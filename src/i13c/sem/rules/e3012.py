from typing import List

from i13c import diag, err
from i13c.sem.graph import Graph
from i13c.sem.model import SemanticModel


def validate_called_arguments_types(
    graph: Graph,
    model: SemanticModel,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in graph.nodes.calls.items():
        by_arity = model.resolver.by_arity.get(cid)
        by_type = model.resolver.by_type.get(cid)

        # if arity was ok but types killed all candidates
        if by_arity and not by_type:
            diagnostics.append(
                err.report_e3012_called_argument_type_mismatch(
                    call.ref,
                    -1,
                    b"<unknown>",
                    b"<unknown>",
                )
            )

    return diagnostics
