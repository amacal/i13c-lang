from typing import List

from i13c import diag, err
from i13c.sem import rel


def validate_called_arguments_types(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, fid in relationships.edges.call_targets.items():
        call = relationships.nodes.calls.get_by_id(cid)

        aids = relationships.edges.call_arguments.get(cid)
        pids = relationships.edges.function_parameters.get(fid)

        # the case is handled by another rule
        if len(aids) != len(pids):
            continue

        # positional matching
        for idx, (aid, pid) in enumerate(zip(aids, pids)):
            atype = relationships.analysis.argument_types.find_by_id(aid)
            ptype = relationships.analysis.parameter_types.find_by_id(pid)

            if atype is None or ptype is None or atype != ptype:
                diagnostics.append(
                    err.report_e3012_called_argument_type_mismatch(
                        call.ref,
                        idx,
                        atype.name if atype else b"<unknown>",
                        ptype.name if ptype else b"<unknown>",
                    )
                )

    return diagnostics
