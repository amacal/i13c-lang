from typing import List

from i13c import diag, err
from i13c.sem import rel


def validate_called_arguments_count(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, fid in relationships.edges.call_targets.items():
        call = relationships.nodes.calls.get_by_id(cid)

        aids = relationships.edges.call_arguments.get(cid)
        pids = relationships.edges.function_parameters.get(fid)

        if len(aids) != len(pids):
            diagnostics.append(
                err.report_e3011_called_argument_count_mismatch(
                    call.ref, len(aids), len(pids)
                )
            )

    return diagnostics
