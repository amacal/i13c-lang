from typing import List, Set

from i13c import diag, err
from i13c.sem import rel


def validate_duplicated_function_clobbers(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, registers in relationships.edges.function_clobbers.items():
        seen: Set[bytes] = set()

        for clobber in registers:
            if clobber.name in seen:
                if function := relationships.nodes.functions.find_by_id(fid):
                    diagnostics.append(
                        err.report_e3005_duplicated_function_clobbers(
                            function.ref,
                            clobber.name,
                        )
                    )
            else:
                seen.add(clobber.name)

    return diagnostics
