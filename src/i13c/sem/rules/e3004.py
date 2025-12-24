from typing import List, Set

from i13c import diag, err
from i13c.sem import rel


def validate_duplicated_parameter_names(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, parameters in relationships.edges.function_parameters.items():
        seen: Set[bytes] = set()

        for pid in parameters:
            if parameter := relationships.nodes.parameters.find_by_id(pid):
                if parameter.name in seen:
                    if function := relationships.nodes.functions.find_by_id(fid):
                        diagnostics.append(
                            err.report_e3004_duplicated_parameter_names(
                                function.ref,
                                parameter.name,
                            )
                        )
                else:
                    seen.add(parameter.name)

    return diagnostics
