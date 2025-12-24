from typing import List, Set

from i13c import diag, err
from i13c.sem import rel


def validate_duplicated_function_names(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    seen: Set[bytes] = set()

    for fid in relationships.nodes.functions.id_to_node:
        if function := relationships.nodes.functions.find_by_id(fid):
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
