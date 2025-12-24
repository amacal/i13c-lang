from typing import List, Set

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_duplicated_parameter_names(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, parameters in graph.edges.function_parameters.items():
        seen: Set[bytes] = set()

        for pid in parameters:
            if parameter := graph.nodes.parameters.find_by_id(pid):
                if parameter.name in seen:
                    if function := graph.nodes.functions.find_by_id(fid):
                        diagnostics.append(
                            err.report_e3004_duplicated_parameter_names(
                                function.ref,
                                parameter.name,
                            )
                        )
                else:
                    seen.add(parameter.name)

    return diagnostics
