from typing import List

from i13c import diag, err
from i13c.sem.analysis import Analysis
from i13c.sem.graph import Graph


def validate_called_arguments_types(
    graph: Graph,
    analysis: Analysis,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, fids in graph.edges.call_targets.items():
        call = graph.nodes.calls.get_by_id(cid)

        aids = graph.edges.call_arguments.get(cid)
        pids = graph.edges.function_parameters.get(fids[0])

        # the case is handled by another rule
        if len(aids) != len(pids):
            continue

        # positional matching
        for idx, (aid, pid) in enumerate(zip(aids, pids)):
            atypes = analysis.argument_types.get(aid)
            ptype = analysis.parameter_types.find_by_id(pid)

            if ptype is None or ptype not in atypes:
                diagnostics.append(
                    err.report_e3012_called_argument_type_mismatch(
                        call.ref,
                        idx,
                        atypes[0].name if atypes else b"<unknown>",
                        ptype.name if ptype else b"<unknown>",
                    )
                )

    return diagnostics
