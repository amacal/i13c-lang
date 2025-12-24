from typing import List

from i13c import ast, diag, err
from i13c.sem import rel


def validate_called_symbol_is_asm(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, call in relationships.nodes.calls.id_to_node.items():
        if fid := relationships.edges.call_targets.find_by_id(cid):
            if target := relationships.nodes.functions.find_by_id(fid):
                if not isinstance(target, ast.AsmFunction):
                    diagnostics.append(
                        err.report_e3009_called_symbol_is_asm(
                            call.ref,
                            call.name,
                        )
                    )

    return diagnostics
