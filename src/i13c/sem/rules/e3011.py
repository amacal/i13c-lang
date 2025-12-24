from typing import List

from i13c import diag, err
from i13c.sem.analysis import Analysis
from i13c.sem.graph import Graph


def validate_called_arguments_count(
    graph: Graph,
    analysis: Analysis,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, fids in graph.edges.call_targets.items():
        call = graph.nodes.calls.get_by_id(cid)

        aids = graph.edges.call_arguments.get(cid)
        pids = graph.edges.function_parameters.get(fids[0])

        if len(aids) != len(pids):
            diagnostics.append(
                err.report_e3011_called_argument_count_mismatch(
                    call.ref, len(aids), len(pids)
                )
            )

    return diagnostics
