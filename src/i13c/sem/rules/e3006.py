from typing import List, Set

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_duplicated_function_names(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    seen: Set[bytes] = set()

    for fid in graph.nodes.functions.id_to_node:
        if function := graph.nodes.functions.find_by_id(fid):
            if function.name in seen:
                diagnostics.append(
                    err.report_e3006_duplicated_function_names(
                        function.ref,
                        function.name,
                    )
                )
            else:
                seen.add(function.name)

    return diagnostics
