from typing import List, Set

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_duplicated_function_clobbers(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, rids in graph.edges.function_clobbers.items():
        seen: Set[bytes] = set()

        for clobber in graph.nodes.registers.find_by_ids(rids):
            if clobber.name in seen:
                if function := graph.nodes.functions.find_by_id(fid):
                    diagnostics.append(
                        err.report_e3005_duplicated_function_clobbers(
                            function.ref,
                            clobber.name,
                        )
                    )
            else:
                seen.add(clobber.name)

    return diagnostics
