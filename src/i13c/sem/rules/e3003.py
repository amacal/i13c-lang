from typing import List, Set

from i13c import diag, err
from i13c.sem import rel


def validate_duplicated_parameter_bindings(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, parameters in relationships.edges.function_parameters.items():
        seen: Set[bytes] = set()

        for pid in parameters:
            if register := relationships.edges.parameter_bindings.find_by_id(pid):
                if register.name in seen:
                    if function := relationships.nodes.functions.find_by_id(fid):
                        diagnostics.append(
                            err.report_e3003_duplicated_parameter_bindings(
                                function.ref,
                                register.name,
                            )
                        )
                else:
                    seen.add(register.name)

    return diagnostics
