from typing import List, Set

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_duplicated_parameter_bindings(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, parameters in graph.edges.function_parameters.items():
        seen: Set[bytes] = set()

        for pid in parameters:
            if rid := graph.edges.parameter_bindings.find_by_id(pid):
                if register := graph.nodes.registers.find_by_id(rid):
                    if register.name in seen:
                        if function := graph.nodes.functions.find_by_id(fid):
                            diagnostics.append(
                                err.report_e3003_duplicated_parameter_bindings(
                                    function.ref,
                                    register.name,
                                )
                            )
                    else:
                        seen.add(register.name)

    return diagnostics
